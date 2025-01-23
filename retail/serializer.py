from rest_framework import serializers

from retail.models import Contact, Member, GRAND_LEVEL, MEMBER_TYPE
from retail.src.field_validators import are_fields_valid


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
           model = Contact
           fields = '__all__'

class ContactWithMemberSerializer(serializers.ModelSerializer):
    class Meta:
           model = Contact
           fields = '__all__'
           extra_kwargs = {
            'member': {'required': False},
           }

class MemberSerializer(serializers.ModelSerializer):
    contacts = ContactWithMemberSerializer(many=True,)

    class Meta:
        model = Member
        fields = ('pk', 'name',  'member_type', 'member_level', 'accounts_payable', 'supplier', 'contacts')
        extra_kwargs = {
            'member_level': {'required': False, 'read_only': True},
            'pk': {'read_only': True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['contacts'] = data['contacts'][:1]
        return data

    def update(self, instance, validated_data):

        rel_obj_validated_data = validated_data.pop('contacts', [])
        rel_validate_data = next(iter(rel_obj_validated_data or []), None)

        rel_obj_data = self.initial_data.get('contacts')
        rel_data = next(iter(rel_obj_data or []), None)

        if rel_validate_data is not None:
            related_obj, created = Contact.objects.get_or_create(
                    pk=rel_data.get('id', None),
                    defaults=rel_validate_data
                )
            if not created:
                for key, value in rel_validate_data.items():
                    setattr(related_obj, key, value)
                related_obj.save()


        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance


    def create(self, validated_data):
        contact_data = validated_data.pop('contacts')
        member = Member.objects.create(**validated_data)
        if member:
            if len(contact_data)>0:
                contact = Contact.objects.get_or_create(member=member, **contact_data[0])

        return member

    def validate(self, data):
        pk = self.instance.pk
        valid, context = are_fields_valid(data, pk)
        if not valid:
            raise serializers.ValidationError(context)

