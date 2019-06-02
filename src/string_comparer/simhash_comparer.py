from src.string_comparer.base import StringComparer
from simhash import Simhash

class SimhashComparer(StringComparer):
    ACCEPTED_PLAGIARISM_KOEF = 15
    @staticmethod
    def compare(str1, str2):
        return Simhash(str1).distance(Simhash(str2)) < SimhashComparer.ACCEPTED_PLAGIARISM_KOEF
