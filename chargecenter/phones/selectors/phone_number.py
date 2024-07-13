from django.contrib.postgres.search import TrigramSimilarity, SearchVector, SearchQuery, SearchRank
from django.db.models import Q

from chargecenter.phones.models import PhoneNumber


def get_phone_numbers(search_param: str = None):
    if not search_param:
        return PhoneNumber.objects.all()
    else:
        trigram_similarity = TrigramSimilarity("name", search_param)
        search_vector = SearchVector("name", weight="A")
        search_query = SearchQuery(search_param)
        return PhoneNumber.objects.all().annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query),
            trigram_similarity=trigram_similarity
        ).filter(Q(trigram_similarity__gte=0.15) | Q(rank__gte=0.1)).distinct().order_by("-trigram_similarity", "-rank")
