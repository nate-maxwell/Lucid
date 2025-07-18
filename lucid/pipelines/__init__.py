"""
# Lucid Domain Pipelines

* Description:

    Pipeline objects are the file io and database handlers for saving, opening, and
    saving files within the pipelines. They handle both database asset registration
    and the disk file operations.
"""


def contains_enum_to_dict(obj: object) -> dict:
    """Converts the __dict__ of an object that contains an enum field to
    something json serializable.
    """
    return {
        key: value.value if isinstance(value, enum.Enum) else value
        for key, value in obj.__dict__.items()
    }
