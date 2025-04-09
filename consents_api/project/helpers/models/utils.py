def get_or_create(cls, get_kwargs, create_kwargs=None):
    try:
        return cls.objects.get(**get_kwargs)
    except cls.DoesNotExist:
        kwargs = create_kwargs if create_kwargs else get_kwargs
        return cls.objects.create(**kwargs)
