package org.matsim.episim.model.vaccination;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Random;
import java.util.SplittableRandom;
import java.util.stream.Collectors;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.population.Person;
import org.matsim.episim.EpisimPerson;
import org.matsim.episim.EpisimUtils;
import org.matsim.episim.InfectionEventHandler;
import org.matsim.episim.VaccinationConfigGroup;
import org.matsim.episim.model.VaccinationType;
import org.matsim.facilities.ActivityFacility;
import org.matsim.vehicles.Vehicle;

import com.google.inject.Inject;

/**
 * Vaccinate people in the population randomly.
 */
public class RandomVaccination implements VaccinationModel {

	private static final Logger log = LogManager.getLogger(RandomVaccination.class);

	private final SplittableRandom rnd;
	private final VaccinationConfigGroup vaccinationConfig;

	@Inject
	public RandomVaccination(SplittableRandom rnd, VaccinationConfigGroup vaccinationConfig) {
		this.rnd = rnd;
		this.vaccinationConfig = vaccinationConfig;
	}

	@Override
	public void init(SplittableRandom rnd, Map<Id<Person>, EpisimPerson> persons, Map<Id<ActivityFacility>, InfectionEventHandler.EpisimFacility> facilities, Map<Id<Vehicle>, InfectionEventHandler.EpisimVehicle> vehicles, LocalDate startDate) {
		int totalVaccinated = 0;
		int totalReVaccinated = 0;
		for(Entry<LocalDate, Integer> e:this.vaccinationConfig.getVaccinationCapacity().entrySet()){
			if(e.getKey().isBefore(startDate)) {
				int vaccineIter = (int)ChronoUnit.DAYS.between( startDate , e.getKey());
				totalVaccinated+=	this.handleVaccination(persons, false,e.getValue(), e.getKey(), vaccineIter, 0);
			}
			
		}
		for(Entry<LocalDate, Integer> e:this.vaccinationConfig.getReVaccinationCapacity().entrySet()){
			if(e.getKey().isBefore(startDate)) {
				int vaccineIter = (int)ChronoUnit.DAYS.between( startDate , e.getKey());
				totalReVaccinated+=this.handleVaccination(persons, true,e.getValue(), e.getKey(), vaccineIter, 0);
			}
			
		}
		log.info("Initial vaccination = "+ totalVaccinated+" and initial revaccination = "+totalReVaccinated);
	}
	@Override
	public int handleVaccination(Map<Id<Person>, EpisimPerson> persons, boolean reVaccination, int availableVaccinations, LocalDate date, int iteration, double now) {

		if (availableVaccinations <= 0)
			return 0;

		Map<VaccinationType, Double> prob = vaccinationConfig.getVaccinationTypeProb(date);

		List<EpisimPerson> candidates = persons.values().stream()
				.filter(EpisimPerson::isVaccinable)
				.filter(p -> p.getDiseaseStatus() == EpisimPerson.DiseaseStatus.susceptible && !p.isRecentlyRecovered(iteration, 180))
				.filter(p -> p.getVaccinationStatus() == (reVaccination ? EpisimPerson.VaccinationStatus.yes : EpisimPerson.VaccinationStatus.no))
				.filter(p -> p.getReVaccinationStatus() == EpisimPerson.VaccinationStatus.no)
				.filter(p -> reVaccination ? p.daysSince(EpisimPerson.VaccinationStatus.yes, iteration) >= vaccinationConfig.getParams(p.getVaccinationType(0)).getBoostWaitPeriod() : true)
				.collect(Collectors.toList());

		if (candidates.isEmpty()) {
			log.warn("Not enough people to vaccinate left ({})", availableVaccinations);
			return 0;
		}

		Collections.shuffle(candidates, new Random(EpisimUtils.getSeed(rnd)));

		int vaccinationsLeft = availableVaccinations;
		int n = Math.min(candidates.size(), vaccinationsLeft);

		for (int i = 0; i < n; i++) {
			EpisimPerson person = candidates.get(i);
			vaccinate(person, iteration, reVaccination ? VaccinationType.mRNA : VaccinationModel.chooseVaccinationType(prob, rnd));
			vaccinationsLeft--;
		}

		return availableVaccinations - vaccinationsLeft;
	}
}
