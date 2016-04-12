class AddonProviderError(Exception):
    """The base class for all addon-related error."""
    pass


class AddonProviderMissingError(AddonProviderError):
    pass


class AddonProviderConfigError(AddonProviderError):
    pass


class AddonProviderImportError(AddonProviderError):
    pass


class AddonProviderInvalidOperationError(AddonProviderError):
    pass
