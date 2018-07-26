from django import forms
from .models import RestaurantLocation


class RestaurantCreateForm(forms.Form):
    name = forms.CharField()
    location = forms.CharField(required=False)
    category = forms.CharField(required=False)

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name == "Hello":
            raise forms.ValidationError("Not a valid name")
        return name


class RestaurantLocationCreateForm(forms.ModelForm):
    class Meta:
        model = RestaurantLocation
        fields = [
            'name',
            'location',
            'category',
            'slug',
        ]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name == "Hello":
            raise forms.ValidationError("Not a valid name")
        return name


# class ItemForm(forms.ModelForm):
#     class Meta:
#         model = Item
#         fields = [
#             'restaurant',
#             'name',
#             'contents',
#             'excludes',
#             'public',
#         ]
#
#     def __init__(self, user=None, *args, **kwargs):
#         # print(kwargs.pop('user'))
#         print(user)
#         super(ItemForm, self).__init__(*args, **kwargs)
#         self.fields['restaurant'].queryset = RestaurantLocation.objects.filter(owner=user, item_isnull=True) # .exclude(item_isnull=False)
