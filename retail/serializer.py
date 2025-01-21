from rest_framework import serializers

from retail.models import Contact, Member


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
           model = Contact
           fields = '__all__'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        a=1


class MemberSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True,)

    class Meta:
        model = Member
        fields = ('name',  'display_member_type', 'member_level', 'accounts_payable', 'supplier', 'contacts')

