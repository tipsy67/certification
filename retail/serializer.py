from rest_framework import serializers
from rest_framework.filters import SearchFilter, OrderingFilter

from retail.models import Contact, Member, Product
from retail.src.field_validators import are_fields_valid



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class ContactWithMemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Contact
        fields = ('id', 'email', 'country', 'city', 'street', 'building', 'member')
        read_only_fields = []


class MemberSerializer(serializers.ModelSerializer):
    contacts = ContactWithMemberSerializer(
        many=True,
    )
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Member
        fields = (
            'id',
            'name',
            'member_type',
            'member_level',
            'accounts_payable',
            'supplier',
            'contacts',
            'products',
        )
        extra_kwargs = {
            'member_level': {'required': False, 'read_only': True},
            'id': {'read_only': True},
            'accounts_payable': {'read_only': True},
        }

    # def to_representation(self, instance):
    #     """Покажем только последний добавленный контакт"""
    #     data = super().to_representation(instance)
    #     data['contacts'] = data['contacts'][:1]
    #     return data

    def update(self, instance, validated_data):

        contacts_validated_data = validated_data.pop('contacts', [])
        # rel_validate_data = next(iter(rel_obj_validated_data or []), None)

        # rel_obj_data = self.initial_data.get('contacts')
        # rel_data = next(iter(rel_obj_data or []), None)
        member_id = instance.id
        # rel_data = Contact.objects.filter(member=member_pk).first()

        for one_contact_validated_data in contacts_validated_data:
            if one_contact_validated_data is not None:
                related_obj, created = Contact.objects.get_or_create(
                    pk=one_contact_validated_data.get('id'),
                    member_id=member_id,
                    defaults=one_contact_validated_data,
                )
                if not created:
                    for key, value in one_contact_validated_data.items():
                        setattr(related_obj, key, value)
                    related_obj.save()

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts')
        member = Member.objects.create(**validated_data)
        if member:
            if len(contacts_data) > 0:
                for one_contact_data in contacts_data:
                    contact = Contact.objects.create(
                        member=member, **one_contact_data
                    )

        return member

    def validate(self, data):
        pk = self.instance.pk
        valid, context = are_fields_valid(data, pk)
        if not valid:
            raise serializers.ValidationError(context)

        return data
