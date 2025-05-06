### CC2 Big Data : enjeux, stockage et extraction

### Lien du GITHUB contenant les résultats et MapReducers de chaque résultats 
https://github.com/6YanIS9/ExamenBIGDATA.git

### Configuration par défaut Hadoop

##### Dans l'invite de commande
```
wget https://files.grouplens.org/datasets/movielens/ml-25m.zip
unzip ml-25m.zip 
```
```
head -n 100 ml-25m/tags.csv  tags_echant.csv
```
```
hdfs dfs -copyFromLocal tags_echant.csv tags_echant.csv
hdfs dfs -copyFromLocal ml-25m/tags.csv tags.csv
```
```
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
```
```
sudo python get-pip.py
pip --version
pip install mrjob
```


#### 1. Nombre de tags pour chaque film

##### MapReduce dans le fichier Python tags_par_film.py
```
from mrjob.job import MRJob
from mrjob.step import MRStep

class MovieTagCounter(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_movie_tags,
                   reducer=self.reducer_count_tags)
        ]

    def mapper_get_movie_tags(self, _, line):
        try:
            userID, movieID, tag, timestamp = line.strip().split(",", 3)
            yield movieID, 1
        except:
            pass  # ignore ligne corrompue

    def reducer_count_tags(self, movieID, counts):
        yield movieID, sum(counts)

if __name__ == '__main__':
    MovieTagCounter.run()
```

##### Dans l'invite de commande
```
touch tags_par_film.py
vi tags_par_film.py
mv tags_par_film.py tags_par_film
hdfs dfs -copyFromLocal tags_par_film.py tags_par_film.py
hdfs dfs -copyFromLocal ml-25m/tags.csv
```

```
python tags_par_film/tags_par_film.py -r hadoop --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar hdfs:///user/maria_dev/tags.csv -o tags_par_film
```

#### 2. Nombre de tags pour chaque utilisateur

##### MapReduce dans le fichier Python tags_par_utilisateur.py
```
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
```

##### Dans l'invite de commande
```
touch tags_par_utilisateur.py
vi tags_par_utilisateur.py
hdfs dfs -copyFromLocal tags_par_film.py tags_par_film.py
```
```
python tags_par_utilisateur/tags_par_utilisateur.py -r hadoop --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar hdfs:///user/maria_dev/tags.csv -o tags_par_utilisateur
```

### Autres configurations Hadoop
#### Taille du bloc par défaut

##### 3. Nombre de blocs occupé par le fichier dans HDFS

###### Dans l'invite de commande
```
hdfs getconf -confKey dfs.block.size
```

##### 4. Nombre de fois que chaque tag a été utilisé pour un film

###### MapReduce dans le fichier Python tags_par_film4.py
```
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
```

###### Dans l'invite de commande
```
touch tags_par_film4.py
vi tags_par_film4.py
hdfs dfs -copyFromLocal tags_par_film.py tags_par_film.py
```
```
python tags_par_film4/tags_par_film4.py -r hadoop --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar hdfs:///user/maria_dev/tags.csv -o tags_par_film4
```
#### Taille du bloc = 64 Mo

```
hdfs dfs -D dfs.blocksize=67108864 -put ml-25m/tags.csv tags_64.csv
```
```
hdfs dfs -get tags_par_film/part-00000 tags_par_film

```

##### 3. Nombre de blocs occupé par le fichier dans HDFS

```
```

##### 4. Nombre de fois que chaque tag a été utilisé pour un film

```
```

### Bonus

#### Nombre de tags introduits par le même utilisateur pour chaque film

##### MapReduce dans le fichier Python tags_par_utilisateur_par_film.py
```
from mrjob.job import MRJob
from mrjob.step import MRStep

class TagsPerMoviePerUser(MRJob):
    def steps(self):
        return [MRStep(mapper=self.mapper,
                       reducer=self.reducer)]

    def mapper(self, _, line):
        try:
            userID, movieID, tag, timestamp = line.strip().split(",", 3)
            key = (movieID, userID)
            yield key, 1
        except:
            pass

    def reducer(self, key, counts):
        yield key, sum(counts)

if __name__ == '__main__':
    TagsPerMoviePerUser.run()
```

##### Dans l'invite de commande
```
touch tags_par_utilisateur_par_film.py
vi tags_par_utilisateur_par_film.py
hdfs dfs -copyFromLocal tags_par_film.py tags_par_film.py
```
```
python tags_par_utilisateur_par_film/tags_par_utilisateur_par_film.py -r hadoop --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar hdfs:///user/maria_dev/tags.csv -o tags_par_utilisateur_par_film
```