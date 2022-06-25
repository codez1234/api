
from database.models import TblSites


def get_sites(value=None):
    z = []
    if value:
        y = value.split(",")
        for i in y:
            z.append(int(i))

    query_set = TblSites.objects.filter(id__in=z)

    return query_set
