# Helper to parse sort query param (?sort=gdp_desc etc.)

def parse_sort(sort: str | None):
    if not sort:
        return ("estimated_gdp", "desc")
    key, _, order = sort.partition("_")
    key_map = {
        "gdp": "estimated_gdp",
        "name": "name",
        "pop": "population",
        "population": "population",
        "exchange": "exchange_rate",
        "region": "region",
    }
    col = key_map.get(key.lower(), "estimated_gdp")
    direction = "desc" if order.lower() == "desc" else "asc"
    return (col, direction)
