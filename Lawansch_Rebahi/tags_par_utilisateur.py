from mrjob.job import MRJob
from mrjob.step import MRStep

class TagsPerUser(MRJob):
    def steps(self):
        return [MRStep(mapper=self.mapper,
                       reducer=self.reducer)]

    def mapper(self, _, line):
        try:
            userID, movieID, tag, timestamp = line.strip().split(",", 3)
            yield userID, 1
        except:
            pass

    def reducer(self, userID, counts):
        yield userID, sum(counts)

if __name__ == '__main__':
    TagsPerUser.run()