from .models import TourVariation
from django import forms
from django.forms.models import modelformset_factory


class TourVariationInventoryForm(forms.ModelForm):
    class Meta:
        model = TourVariation
        fields = [
            "price",
            "sale_price",
            "inventory",
            "active"
        ]

TourVariationInventoryFormSet = modelformset_factory(TourVariation, form=TourVariationInventoryForm, extra=0)
