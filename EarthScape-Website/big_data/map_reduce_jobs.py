from mrjob.job import MRJob
from mrjob.step import MRStep


class MRClimateAnalysis(MRJob):
    """
    A MapReduce Job to calculate the Average Temperature per Year.
    Requirement: "Implement Hadoop MapReduce jobs for parallel processing"
    """

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper_extract_year_temp, reducer=self.reducer_calculate_avg
            )
        ]

    def mapper_extract_year_temp(self, _, line):
        # Skip header line
        if "AverageTemperature" in line:
            return

        # Data format: dt, AverageTemperature, Uncertainty, City, Country, ...
        fields = line.split(",")
        try:
            date = fields[0]
            temp = fields[1]

            # Extract Year from Date (YYYY-MM-DD)
            year = date.split("-")[0]

            if temp and year:
                yield year, float(temp)
        except:
            pass  # Skip malformed lines

    def reducer_calculate_avg(self, year, temps):
        # Calculate average for the year
        total = 0
        count = 0
        for t in temps:
            total += t
            count += 1

        if count > 0:
            yield year, round(total / count, 2)


if __name__ == "__main__":
    MRClimateAnalysis.run()
