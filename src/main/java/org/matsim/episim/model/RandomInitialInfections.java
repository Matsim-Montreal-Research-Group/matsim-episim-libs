package org.matsim.episim.model;

import com.google.common.collect.Lists;
import com.google.inject.Inject;
import it.unimi.dsi.fastutil.objects.Object2IntAVLTreeMap;
import it.unimi.dsi.fastutil.objects.Object2IntMap;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.population.Person;
import org.matsim.core.config.Config;
import org.matsim.core.config.ConfigUtils;
import org.matsim.episim.EpisimConfigGroup;
import org.matsim.episim.EpisimPerson;
import org.matsim.episim.EpisimUtils;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;
import java.util.NavigableMap;
import java.util.SplittableRandom;
import java.util.stream.Collectors;

/**
 * Randomly infect persons, optionally filtering by age group and district.
 */
public class RandomInitialInfections implements InitialInfectionHandler {

	private static final Logger log = LogManager.getLogger(RandomInitialInfections.class);

	private final EpisimConfigGroup episimConfig;
	private final SplittableRandom rnd;

	private int initialInfectionsLeft;

	@Inject
	public RandomInitialInfections(Config config, SplittableRandom rnd) {
		this.episimConfig = ConfigUtils.addOrGetModule(config, EpisimConfigGroup.class);
		this.rnd = rnd;
	}

	@Override
	public Object2IntMap<VirusStrain> handleInfections(Map<Id<Person>, EpisimPerson> persons, int iteration) {

		if (initialInfectionsLeft == 0) return new Object2IntAVLTreeMap<>();

		double now = EpisimUtils.getCorrectedTime(episimConfig.getStartOffset(), 0, iteration);

		String district = episimConfig.getInitialInfectionDistrict();

		int lowerAgeBoundaryForInitInfections = episimConfig.getLowerAgeBoundaryForInitInfections();
		int upperAgeBoundaryForInitInfections = episimConfig.getUpperAgeBoundaryForInitInfections();

		LocalDate date = episimConfig.getStartDate().plusDays(iteration - 1);

//		int infected = 0;
		Object2IntMap<VirusStrain> infectedByStrain = new Object2IntAVLTreeMap<>();

		for (Map.Entry<VirusStrain, NavigableMap<LocalDate, Integer>> e : episimConfig.getInfections_pers_per_day().entrySet()) {

			infectedByStrain.put(e.getKey(), 0);

			int defInf = 0;
			if(infectedByStrain.size()==0) defInf = 1;
			int numInfections = EpisimUtils.findValidEntry(e.getValue(), defInf, date);
			

			List<EpisimPerson> candidates = persons.values().stream()
					.filter(p -> district == null || district.equals(p.getAttributes().getAttribute("district")))
					.filter(p -> lowerAgeBoundaryForInitInfections == -1 || (int) p.getAttributes().getAttribute("microm:modeled:age") >= lowerAgeBoundaryForInitInfections)
					.filter(p -> upperAgeBoundaryForInitInfections == -1 || (int) p.getAttributes().getAttribute("microm:modeled:age") <= upperAgeBoundaryForInitInfections)
					.filter(p -> p.getDiseaseStatus() == EpisimPerson.DiseaseStatus.susceptible)
					.collect(Collectors.toList());

			if (candidates.size() < numInfections) {
				log.warn("Not enough persons match the initial infection requirement, using whole population...");
				candidates = Lists.newArrayList(persons.values());
			}

			while (numInfections > 0 && initialInfectionsLeft > 0 && candidates.size() > 0) {
				EpisimPerson randomPerson = candidates.remove(rnd.nextInt(candidates.size()));
				if (randomPerson.getDiseaseStatus() == EpisimPerson.DiseaseStatus.susceptible) {
					randomPerson.setInitialInfection(now, e.getKey());
					log.warn("Person {} has initial infection with {}.", randomPerson.getPersonId(), e.getKey());
					initialInfectionsLeft--;
					numInfections--;
					infectedByStrain.merge(e.getKey(), 1, Integer::sum);
//					infected++;

				}
			}
		}


		return infectedByStrain;
	}

	@Override
	public int getInfectionsLeft() {
		return initialInfectionsLeft;
	}

	@Override
	public void setInfectionsLeft(int num) {
		initialInfectionsLeft = num;
	}
}
