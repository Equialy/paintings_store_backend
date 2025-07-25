ALLOWED_SORT_FIELDS = {"id", "title", "author", "quantity", "price"}


def get_sort_column(model, column_name: str):
    if column_name not in ALLOWED_SORT_FIELDS:
        raise ValueError(f"Sorting by '{column_name}' is not allowed.")
    return getattr(model, column_name)
