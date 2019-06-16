from simhash import Simhash

SIMHASH_HIGH_WATERMARK = 30

def convert_to_percents(distance):
    return distance * 100 / SIMHASH_HIGH_WATERMARK

class SimhashComparer:
    @staticmethod
    def compare(str1, str2):
        return 100 - convert_to_percents(
            Simhash(str1).distance(Simhash(str2))
        )
