from mrjob.job import MRJob
from mrjob.step import MRStep

class TagsPerMovie(MRJob):
    def steps(self):
        return [MRStep(mapper=self.mapper,
                       reducer=self.reducer)]

    def mapper(self, _, line):
        try:
            userID, movieID, tag, timestamp = line.strip().split(",", 3)
            yield movieID, 1
        except:
            pass

    def reducer(self, movieID, counts):
        yield movieID, sum(counts)

if __name__ == '__main__':
    TagsPerMovie.run()