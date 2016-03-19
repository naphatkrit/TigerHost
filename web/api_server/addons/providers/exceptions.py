class AddonProviderError(Exception):
    pass


class AddonProviderMissingError(AddonProviderError):
    pass


class AddonProviderConfigError(AddonProviderError):
    pass


class AddonProviderImportError(AddonProviderError):
    pass


class AddonProviderInvalidOperationError(AddonProviderError):
    pass
