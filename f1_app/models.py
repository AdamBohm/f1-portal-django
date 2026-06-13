from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

# 1. TABULKA: Země (Státy)
class Country(models.Model):
    nazev = models.CharField(max_length=100, unique=True, verbose_name="Název země")
    kod = models.CharField(max_length=3, unique=True, verbose_name="Kód země (např. GBR)")
    
    # Použijeme URLField pro odkaz na obrázek vlajky na internetu (ušetří to složité nastavování uploadu obrázků)
    vlajka_url = models.URLField(blank=True, null=True, verbose_name="URL adresa vlajky (např. z Wikipedie)")

    class Meta:
        verbose_name = "Země"
        verbose_name_plural = "Země"
        ordering = ['nazev']

    def __str__(self):
        return f"{self.nazev} ({self.kod})"

# 2. TABULKA: Závodní okruhy
class Track(models.Model):
    nazev = models.CharField(max_length=100, verbose_name="Název okruhu")
    
    # Každý okruh leží v jedné zemi
    zeme = models.ForeignKey(Country, on_delete=models.RESTRICT, verbose_name="Země")
    
    # Změna z CharField na DecimalField pro přesná desetinná čísla (např. 5.412 km)
    delka_km = models.DecimalField(max_digits=5, decimal_places=3, verbose_name="Délka okruhu (km)")

    class Meta:
        verbose_name = "Okruh"
        verbose_name_plural = "Okruhy"

    def __str__(self):
        return f"{self.nazev} - {self.delka_km} km"

# 3. TABULKA: Týmy F1
class Team(models.Model):
    nazev = models.CharField(max_length=100, unique=True, verbose_name="Název týmu")
    sef = models.CharField(max_length=100, verbose_name="Šéf týmu")
    
    # Tým závodí pod určitou národní licencí
    zeme = models.ForeignKey(Country, on_delete=models.RESTRICT, verbose_name="Licence (Země)")
    
    # Přísná validace (RegexValidator) ověří, že uživatel zadá přesně kód barvy se znakem křížku a šesti znaky
    barva_hex = models.CharField(
        max_length=7, 
        default="#FF0000", 
        validators=[RegexValidator(regex='^#[a-fA-F0-9]{6}$', message='Zadejte platný HEX kód (např. #FF0000)')],
        verbose_name="HEX barva týmu"
    )

    class Meta:
        verbose_name = "Tým"
        verbose_name_plural = "Týmy"

    def __str__(self):
        return self.nazev

# 4. TABULKA: Jezdci
class Driver(models.Model):
    jmeno = models.CharField(max_length=100, verbose_name="Jméno jezdce")
    
    # Validace startovního čísla (v F1 je to vždy číslo od 1 do 99)
    cislo = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        unique=True, # Žádní dva jezdci nemohou mít v F1 stejné číslo
        verbose_name="Startovní číslo"
    )
    
    tym = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='jezdci', verbose_name="Tým")
    
    # Národnost jezdce
    zeme = models.ForeignKey(Country, on_delete=models.RESTRICT, verbose_name="Národnost")

    class Meta:
        verbose_name = "Jezdec"
        verbose_name_plural = "Jezdci"
        ordering = ['cislo']

    def __str__(self):
        return f"{self.jmeno} #{self.cislo}"

# 5. TABULKA: Závody (Kalendář)
class Race(models.Model):
    okruh = models.ForeignKey(Track, on_delete=models.CASCADE, verbose_name="Závodní okruh")
    datum = models.DateField(verbose_name="Datum závodu")
    
    # NOVÉ POLE: Propojení na jezdce, který závod vyhrál
    vitez = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='vyhrane_zavody', verbose_name="Vítěz závodu")
    
    nejrychlejsi_kolo_cas = models.CharField(max_length=10, blank=True, null=True, verbose_name="Čas nejrychlejšího kola (např. 1:23.456)")
    
    # UPRAVENO: Přidali jsme related_name='nejrychlejsi_kola', abychom je mohli snadno spočítat
    nejrychlejsi_kolo_jezdec = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='nejrychlejsi_kola', verbose_name="Jezdec s nejrychlejším kolem")

    class Meta:
        verbose_name = "Závod"
        verbose_name_plural = "Závody"
        ordering = ['datum']
        constraints = [
            models.UniqueConstraint(fields=['okruh', 'datum'], name='unique_race_per_day')
        ]

    def __str__(self):
        return f"Velká cena - {self.okruh.zeme.nazev} ({self.datum.year})"