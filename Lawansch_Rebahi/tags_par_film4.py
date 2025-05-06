from mrjob.job import MRJob
from mrjob.step import MRStep

class TagUsageCount(MRJob):
    def steps(self):
        return [MRStep(mapper=self.mapper,
                       reducer=self.reducer)]

    def mapper(self, _, line):
        try:
            userID, movieID, tag, timestamp = line.strip().split(",", 3)
            yield tag.strip().lower(), 1
        except:
            pass

    def reducer(self, tag, counts):
        yield tag, sum(counts)

if __name__ == '__main__':
    TagUsageCount.run()
