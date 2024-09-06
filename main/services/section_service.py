from django.contrib.auth import get_user_model

from main.models import Section, Currency, SectionUser


class SectionService:

    @staticmethod
    def get_or_create_base_section_by_user(
            user: get_user_model(),
            default_currency_code: str = 'USD',
            default_section_name: str = 'Home',
    ) -> tuple[Section, bool]:

        try:
            section = Section.objects.get(
                sectionuser__user=user,
                sectionuser__is_base=True,
            )
            is_created = False
        except SectionUser.DoesNotExist:
            currency, _ = Currency.objects.get_or_create(code=default_currency_code)
            section = Section.objects.create(
                name=default_section_name,
                currency=currency,
            )
            section_user = SectionUser.set_base_section_for_user(user=user, section=section, is_owner=True)
            is_created = True

        return section, is_created
