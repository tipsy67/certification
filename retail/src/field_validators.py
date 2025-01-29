from retail.models import GRAND_LEVEL, GRAND_NAME, MEMBER_TYPE
from retail.src.utils import get_buyers_list


def are_fields_valid(data: dict, pk: int) -> (bool, str | None):
    """Валидация полей для админ панели и API"""
    # pk = data.get('pk',None)
    supplier = data.get('supplier', None)
    member_type = data.get('member_type', None)

    if member_type is not None and member_type != GRAND_LEVEL and supplier is None:
        context = (
            f"Параметр 'supplier'(поставщик) обязателен для типа организации,"
            f" отличной от типа '{GRAND_LEVEL}'({GRAND_NAME})"
        )
        return False, context

    if (member_type is None or member_type == GRAND_LEVEL) and supplier is not None:
        context = (
            f"Параметр 'supplier'(поставщик) должен быть 'null' если 'member_type'"
            f"(тип звена)='{GRAND_LEVEL}'({GRAND_NAME}) или 'null' "
        )
        return False, context

    if pk and supplier:
        if pk == supplier.pk:
            context = "Поставщик не может ссылаться сам на себя"
            return False, context

        if supplier in get_buyers_list(pk):
            context = "Циклические ссылки в сети не допустимы"
            return False, context

    return True, None
