from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from retail.models import City, Contact, Country, Member
from users.models import User


class MemberTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.country = Country.objects.create(name="country")
        cls.city = City.objects.create(name="city")
        cls.member = Member.objects.create(name="Member", member_type="RTL")
        cls.contact = Contact.objects.create(
            email="test@test.test",
            country=cls.country,
            city=cls.city,
            street="street",
            building="building",
            member=cls.member,
        )

        cls.etalon_data = [
            {
                'id': cls.member.pk,
                'name': 'Member',
                'member_type': 'RTL',
                'member_level': 0,
                'accounts_payable': '0.00',
                'supplier': None,
                'contacts': [
                    {
                        'id': cls.contact.pk,
                        'email': 'test@test.test',
                        'country': 'country',
                        'city': 'city',
                        'street': 'street',
                        'building': 'building',
                        'member': cls.member.pk,
                    }
                ],
                'products': [],
            }
        ]

        cls.user = User.objects.create_user(
            username="test_user", password="test_user_password"
        )

    def setUp(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_member_list(self):
        url = reverse("retail:member-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data, self.etalon_data)

    def test_lesson_view(self):
        url = reverse("retail:member-detail", args=(self.member.pk,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data, self.etalon_data[0])

    def test_lesson_update(self):
        url = reverse("retail:member-detail", args=(self.member.pk,))
        data = {"name": "Test update"}

        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data.get("name"), "Test update")

    def test_lesson_destroy(self):
        url = reverse("retail:member-detail", args=(self.member.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Member.objects.all().count(), 0)

    def test_lesson_create(self):
        url = reverse("retail:member-list")

        data = {
            "name": "Mazongo",
            "contacts": [
                {
                    "email": "test@test.test",
                    "country": "country",
                    "city": "city",
                    "street": "street",
                    "building": "building",
                }
            ],
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Member.objects.all().count(), 2)


class AdditionalTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.country = Country.objects.create(name="country")
        cls.city = City.objects.create(name="city")
        cls.member1 = Member.objects.create(name="Member1", member_type="PLNT")
        cls.member2 = Member.objects.create(
            name="Member2", member_type="RTL", supplier=cls.member1
        )
        cls.member3_1 = Member.objects.create(
            name="Member3_1", member_type="INDV", supplier=cls.member2
        )
        cls.member3_2 = Member.objects.create(
            name="Member3_2", member_type="INDV", supplier=cls.member2
        )
        cls.member4 = Member.objects.create(
            name="Member4", member_type="INDV", supplier=cls.member3_1
        )

        cls.contact = Contact.objects.create(
            email="test@test.test",
            country=cls.country,
            city=cls.city,
            street="street",
            building="building",
            member=cls.member1,
        )

        cls.user = User.objects.create_user(
            username="test_user", password="test_user_password"
        )

    def setUp(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_check_validate(self):
        url = reverse("retail:member-detail", args=(self.member1.pk,))
        # check 1
        print("check 1 -------------------------")
        data = {"member_type": "RTL"}

        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertEqual(
            response_data,
            {
                'non_field_errors': [
                    "Параметр 'supplier'(поставщик) обязателен для типа организации, отличной от типа 'PLNT'(Завод)"
                ]
            },
        )

        # check 2
        print("check 2 -------------------------")
        url = reverse("retail:member-detail", args=(self.member1.pk,))
        data = {"supplier": f"{self.member1.pk}"}

        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertEqual(
            response_data,
            {
                'non_field_errors': [
                    "Параметр 'supplier'(поставщик) должен быть 'null' если 'member_type'(тип звена)='PLNT'(Завод) или 'null' "
                ]
            },
        )

        # check 3
        print("check 3 -------------------------")
        data = {"member_type": "RTL", "supplier": f"{self.member1.pk}"}

        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertEqual(
            response_data,
            {'non_field_errors': ['Поставщик не может ссылаться сам на себя']},
        )

        # check 3
        print("check 4 -------------------------")
        data = {"member_type": "RTL", "supplier": f"{self.member4.pk}"}

        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertEqual(
            response_data,
            {'non_field_errors': ['Циклические ссылки в сети не допустимы']},
        )

    def test_check_recalc(self):
        url = reverse("retail:member-detail", args=(self.member2.pk,))
        # check recalc member level
        print("check recalc member level --------")
        data = {"member_type": "PLNT"}

        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        obj = Member.objects.filter(pk=self.member2.pk).first()
        self.assertEqual(getattr(obj, 'member_level'), 0)

        obj = Member.objects.filter(pk=self.member3_1.pk).first()
        self.assertEqual(getattr(obj, 'member_level'), 1)

        obj = Member.objects.filter(pk=self.member3_2.pk).first()
        self.assertEqual(getattr(obj, 'member_level'), 1)

        obj = Member.objects.filter(pk=self.member4.pk).first()
        self.assertEqual(getattr(obj, 'member_level'), 2)
