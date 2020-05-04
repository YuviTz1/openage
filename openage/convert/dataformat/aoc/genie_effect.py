# Copyright 2019-2020 the openage authors. See copying.md for legal info.

from ...dataformat.converter_object import ConverterObject


class GenieEffectObject(ConverterObject):
    """
    Single effect contained in GenieEffectBundle.
    """

    __slots__ = ('bundle_id', 'data')

    def __init__(self, effect_id, bundle_id, full_data_set, members=None):
        """
        Creates a new Genie effect object.

        :param effect_id: The index of the effect in the .dat file's effect
        :param bundle_id: The index of the effect bundle that the effect belongs to.
                          (the index is referenced as tech_effect_id by techs)
        :param full_data_set: GenieObjectContainer instance that
                              contains all relevant data for the conversion
                              process.
        :param members: An already existing member dict.
        """

        super().__init__(effect_id, members=members)

        self.bundle_id = bundle_id
        self.data = full_data_set

    def get_type(self):
        """
        Returns the effect's type.
        """
        return self.get_member("type_id").get_value()

    def __repr__(self):
        return "GenieEffectObject<%s>" % (self.get_id())


class GenieEffectBundle(ConverterObject):
    """
    A set of effects of a tech.
    """

    __slots__ = ('effects', 'sanitized', 'data')

    def __init__(self, bundle_id, effects, full_data_set, members=None):
        """
        Creates a new Genie effect bundle.

        :param bundle_id: The index of the effect in the .dat file's effect
                          block. (the index is referenced as tech_effect_id by techs)
        :param effects: Effects of the bundle as list of GenieEffectObject.
        :param full_data_set: GenieObjectContainer instance that
                              contains all relevant data for the conversion
                              process.
        :param members: An already existing member dict.
        """

        super().__init__(bundle_id, members=members)

        self.effects = effects

        # Sanitized bundles should not contain 'garbage' effects, e.g.
        #     - effects that do nothing
        #     - effects without a type        #
        # Processors should set this to True, once the bundle is sanitized.
        self.sanitized = False

        self.data = full_data_set

    def get_effects(self, effect_type=None):
        """
        Returns the effects in the bundle, optionally only effects with a specific
        type.

        :param effect_type: Type that the effects should have.
        :type effect_type: int, optional
        :returns: List of matching effects.
        :rtype: list
        """
        if effect_type:
            matching_effects = []
            for effect in self.effects.values():
                if effect.get_type() == effect_type:
                    matching_effects.append(effect)

            return matching_effects

        else:
            return list(self.effects.values())

    def is_sanitized(self):
        """
        Returns whether the effect bundle has been sanitized.
        """
        return self.sanitized

    def __repr__(self):
        return "GenieEffectBundle<%s>" % (self.get_id())
