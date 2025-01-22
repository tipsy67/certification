from rest_framework import serializers

from retail.models import Contact, Member


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
           model = Contact
           fields = '__all__'


class MemberSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True,)

    class Meta:
        model = Member
        fields = ('pk', 'name',  'display_member_type', 'member_level', 'accounts_payable', 'supplier', 'contacts')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['contacts'] = data['contacts'][:1]
        return data

    def update(self, instance, validated_data):
        if self.is_valid():
            pass
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