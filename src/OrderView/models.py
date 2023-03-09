from django.db import models


class Skany(models.Model):
    indeks = models.IntegerField(
        db_column="Indeks", primary_key=True
    )  # Field name made lowercase.
    archiwum = models.IntegerField(
        db_column="Archiwum", blank=True, null=True
    )  # Field name made lowercase.
    data = models.DateTimeField(
        db_column="Data", blank=True, null=True
    )  # Field name made lowercase.
    del_field = models.IntegerField(
        db_column="Del", blank=True, null=True
    )  # Field name made lowercase. Field renamed because it was a Python reserved word.
    kodkreskowy = models.CharField(
        db_column="KodKreskowy",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    oscieznica = models.IntegerField(
        db_column="Oscieznica", blank=True, null=True
    )  # Field name made lowercase.
    pozycja = models.IntegerField(
        db_column="Pozycja", blank=True, null=True
    )  # Field name made lowercase.
    skrzydlo = models.IntegerField(
        db_column="Skrzydlo", blank=True, null=True
    )  # Field name made lowercase.
    srcdoc = models.IntegerField(blank=True, null=True)
    stanowisko = models.IntegerField(
        db_column="Stanowisko", blank=True, null=True
    )  # Field name made lowercase.
    sztuka = models.IntegerField(
        db_column="Sztuka", blank=True, null=True
    )  # Field name made lowercase.
    uzytkownik = models.IntegerField(
        db_column="Uzytkownik", blank=True, null=True
    )  # Field name made lowercase.
    zakonczony = models.IntegerField(
        db_column="Zakonczony", blank=True, null=True
    )  # Field name made lowercase.
    czynnosc = models.IntegerField(
        db_column="Czynnosc", blank=True, null=True
    )  # Field name made lowercase.
    dbwhokna = models.IntegerField(
        db_column="DbWHOkna", blank=True, null=True
    )  # Field name made lowercase.
    guid = models.CharField(
        db_column="Guid",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    guidparent = models.CharField(
        db_column="GuidParent",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    status = models.IntegerField(
        db_column="Status", blank=True, null=True
    )  # Field name made lowercase.
    typ = models.IntegerField(
        db_column="Typ", blank=True, null=True
    )  # Field name made lowercase.
    typslupka = models.IntegerField(
        db_column="TypSlupka", blank=True, null=True
    )  # Field name made lowercase.
    erridx = models.IntegerField(
        db_column="ErrIdx", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "Skany"


class SkanyVsZlecenia(models.Model):
    indeks = models.IntegerField(
        db_column="Indeks", primary_key=True
    )  # Field name made lowercase.
    indeksskanu = models.IntegerField(
        db_column="IndeksSkanu", blank=True, null=True
    )  # Field name made lowercase.
    indekszlecenia = models.IntegerField(
        db_column="IndeksZlecenia", blank=True, null=True
    )  # Field name made lowercase.
    indeksdodatka = models.CharField(
        db_column="IndeksDodatka",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    duplicated = models.IntegerField(
        db_column="Duplicated", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "Skany_vs_Zlecenia"


class Stanowiska(models.Model):
    indeks = models.IntegerField(
        db_column="Indeks", primary_key=True
    )  # Field name made lowercase.
    aktywny = models.IntegerField(
        db_column="Aktywny", blank=True, null=True
    )  # Field name made lowercase.
    data = models.DateTimeField(
        db_column="Data", blank=True, null=True
    )  # Field name made lowercase.
    del_field = models.IntegerField(
        db_column="Del", blank=True, null=True
    )  # Field name made lowercase. Field renamed because it was a Python reserved word.
    drukujraport = models.CharField(
        db_column="DrukujRaport",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    liczbaporzadkowa = models.IntegerField(
        db_column="LiczbaPorzadkowa", blank=True, null=True
    )  # Field name made lowercase.
    liniaprodukcyjna = models.IntegerField(
        db_column="LiniaProdukcyjna", blank=True, null=True
    )  # Field name made lowercase.
    obslugastojakow = models.IntegerField(
        db_column="ObslugaStojakow", blank=True, null=True
    )  # Field name made lowercase.
    opis = models.CharField(
        db_column="Opis",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    opisczynnosci = models.CharField(
        db_column="OpisCzynnosci",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    podstatusprzed = models.CharField(
        db_column="PodstatusPrzed",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    podstatuspo = models.CharField(
        db_column="PodstatusPo",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    raport = models.CharField(
        db_column="Raport",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    raportdodatki = models.CharField(
        db_column="RaportDodatki",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    rozwintabelke = models.IntegerField(
        db_column="RozwinTabelke", blank=True, null=True
    )  # Field name made lowercase.
    skanowanie = models.IntegerField(
        db_column="Skanowanie", blank=True, null=True
    )  # Field name made lowercase.
    stanowiskokoncowe = models.IntegerField(
        db_column="StanowiskoKoncowe", blank=True, null=True
    )  # Field name made lowercase.
    wielkoscczcionki = models.IntegerField(
        db_column="WielkoscCzcionki", blank=True, null=True
    )  # Field name made lowercase.
    zdejmowanie = models.IntegerField(
        db_column="Zdejmowanie", blank=True, null=True
    )  # Field name made lowercase.
    zliczanie = models.IntegerField(
        db_column="Zliczanie", blank=True, null=True
    )  # Field name made lowercase.
    zoom1 = models.IntegerField(
        db_column="Zoom1", blank=True, null=True
    )  # Field name made lowercase.
    zoom2 = models.IntegerField(
        db_column="Zoom2", blank=True, null=True
    )  # Field name made lowercase.
    proceduraskladowa = models.IntegerField(
        db_column="ProceduraSkladowa", blank=True, null=True
    )  # Field name made lowercase.
    viewer = models.CharField(
        db_column="Viewer",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    czynnoscosc = models.IntegerField(
        db_column="CzynnoscOsc", blank=True, null=True
    )  # Field name made lowercase.
    czynnoscskr = models.IntegerField(
        db_column="CzynnoscSkr", blank=True, null=True
    )  # Field name made lowercase.
    czynnoscslr = models.IntegerField(
        db_column="CzynnoscSlr", blank=True, null=True
    )  # Field name made lowercase.
    czynnoscsls = models.IntegerField(
        db_column="CzynnoscSls", blank=True, null=True
    )  # Field name made lowercase.
    czynnoscszkl = models.IntegerField(
        db_column="CzynnoscSzkl", blank=True, null=True
    )  # Field name made lowercase.
    obslugatransportu = models.IntegerField(
        db_column="ObslugaTransportu", blank=True, null=True
    )  # Field name made lowercase.
    barcodeidx = models.IntegerField(
        db_column="BarcodeIdx", blank=True, null=True
    )  # Field name made lowercase.
    barcodeprevidx = models.IntegerField(
        db_column="BarcodePrevIdx", blank=True, null=True
    )  # Field name made lowercase.
    barcodenextidx = models.IntegerField(
        db_column="BarcodeNextIdx", blank=True, null=True
    )  # Field name made lowercase.
    cursortimeout = models.IntegerField(
        db_column="CursorTimeout", blank=True, null=True
    )  # Field name made lowercase.
    defaultevent = models.IntegerField(
        db_column="DefaultEvent", blank=True, null=True
    )  # Field name made lowercase.
    tablefilter = models.IntegerField(
        db_column="TableFilter", blank=True, null=True
    )  # Field name made lowercase.
    panelinfowidth = models.IntegerField(
        db_column="PanelInfoWidth", blank=True, null=True
    )  # Field name made lowercase.
    printer = models.CharField(
        db_column="Printer",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    raportstojaki = models.CharField(
        db_column="RaportStojaki",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    zoomstands = models.IntegerField(
        db_column="ZoomStands", blank=True, null=True
    )  # Field name made lowercase.
    middle = models.IntegerField(
        db_column="Middle", blank=True, null=True
    )  # Field name made lowercase.
    middle_type = models.IntegerField(
        db_column="Middle_type", blank=True, null=True
    )  # Field name made lowercase.
    obslugasektorow = models.IntegerField(
        db_column="ObslugaSektorow", blank=True, null=True
    )  # Field name made lowercase.
    userdescription = models.CharField(
        db_column="UserDescription",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    userstatus = models.CharField(
        db_column="UserStatus",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    canhavedifferentip = models.CharField(
        db_column="CanHaveDifferentIP",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    qualitycontrolworkplace = models.CharField(
        db_column="QualityControlWorkplace",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    alvarchar = models.CharField(
        db_column="AlVARCHAR",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    altextrasworkplace = models.IntegerField(
        db_column="AlTEXTrasWorkplace", blank=True, null=True
    )  # Field name made lowercase.
    allowglassscan = models.IntegerField(
        db_column="AllowGlassScan", blank=True, null=True
    )  # Field name made lowercase.
    onlyoneworkeronthisworkplace = models.IntegerField(
        db_column="OnlyOneWorkerOnThisWorkplace", blank=True, null=True
    )  # Field name made lowercase.
    altextrasdatecolumnname = models.CharField(
        db_column="AlTEXTrasDateColumnName",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    hidelaborbutton = models.IntegerField(
        db_column="HideLaborButton", blank=True, null=True
    )  # Field name made lowercase.
    importpackagestoszybyxls = models.IntegerField(
        db_column="ImportPackagesToSzybyXLS", blank=True, null=True
    )  # Field name made lowercase.
    hidetableinpackagesloading = models.IntegerField(
        db_column="HideTableInPackagesLoading", blank=True, null=True
    )  # Field name made lowercase.
    altcuttingworkplace = models.IntegerField(
        db_column="AltCuttingWorkplace", blank=True, null=True
    )  # Field name made lowercase.
    mobile = models.IntegerField(
        db_column="Mobile", blank=True, null=True
    )  # Field name made lowercase.
    markwhentransportispacked = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Stanowiska"


class Uzytkownicy(models.Model):
    indeks = models.IntegerField(
        db_column="Indeks", primary_key=True
    )  # Field name made lowercase.
    aktywny = models.IntegerField(
        db_column="Aktywny", blank=True, null=True
    )  # Field name made lowercase.
    data = models.DateTimeField(
        db_column="Data", blank=True, null=True
    )  # Field name made lowercase.
    dealer = models.CharField(
        db_column="Dealer",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    del_field = models.IntegerField(
        db_column="Del", blank=True, null=True
    )  # Field name made lowercase. Field renamed because it was a Python reserved word.
    haslo = models.CharField(
        db_column="Haslo",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    imie = models.CharField(
        db_column="Imie",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    login = models.CharField(
        db_column="Login",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    nazwa = models.CharField(
        db_column="Nazwa",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    nazwisko = models.CharField(
        db_column="Nazwisko",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    nip = models.CharField(
        db_column="Nip",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    uprawnienia = models.IntegerField(
        db_column="Uprawnienia", blank=True, null=True
    )  # Field name made lowercase.
    usr = models.IntegerField(
        db_column="Usr", blank=True, null=True
    )  # Field name made lowercase.
    uwagi = models.CharField(
        db_column="Uwagi",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    stawkadzienna = models.IntegerField(
        db_column="StawkaDzienna", blank=True, null=True
    )  # Field name made lowercase.
    barcodeidx = models.IntegerField(
        db_column="BarcodeIdx", blank=True, null=True
    )  # Field name made lowercase.
    language = models.CharField(
        db_column="Language",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    grupaplacowa = models.IntegerField(
        db_column="GrupaPlacowa", blank=True, null=True
    )  # Field name made lowercase.
    tworzenieartykulow = models.IntegerField(
        db_column="TworzenieArtykulow", blank=True, null=True
    )  # Field name made lowercase.
    email = models.CharField(
        db_column="Email",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    zestawieniezlecennaprodukcjivisible = models.IntegerField(
        db_column="ZestawienieZlecenNaProdukcjiVisible", blank=True, null=True
    )  # Field name made lowercase.
    zawartoscstojakowvisible = models.IntegerField(
        db_column="ZawartoscStojakowVisible", blank=True, null=True
    )  # Field name made lowercase.
    zawartoscsamochodowvisible = models.IntegerField(
        db_column="ZawartoscSamochodowVisible", blank=True, null=True
    )  # Field name made lowercase.
    zawartoscsektorowvisible = models.IntegerField(
        db_column="ZawartoscSektorowVisible", blank=True, null=True
    )  # Field name made lowercase.
    zawartoscsektorowszkleniavisible = models.IntegerField(
        db_column="ZawartoscSektorowSzkleniaVisible", blank=True, null=True
    )  # Field name made lowercase.
    zestawienieczynnoscivisible = models.IntegerField(
        db_column="ZestawienieCzynnosciVisible", blank=True, null=True
    )  # Field name made lowercase.
    zestawienieodpowiedzinapytaniavisible = models.IntegerField(
        db_column="ZestawienieOdpowiedziNaPytaniaVisible", blank=True, null=True
    )  # Field name made lowercase.
    zestawienierobociznyvisible = models.IntegerField(
        db_column="ZestawienieRobociznyVisible", blank=True, null=True
    )  # Field name made lowercase.
    zestawieniebledowkomunikatownotatekvisible = models.IntegerField(
        db_column="ZestawienieBledowKomunikatowNotatekVisible", blank=True, null=True
    )  # Field name made lowercase.
    eksportwykonanychoscieznicvisible = models.IntegerField(
        db_column="EksportWykonanychOscieznicVisible", blank=True, null=True
    )  # Field name made lowercase.
    posteprealizacjivisible = models.IntegerField(
        db_column="PostepRealizacjiVisible", blank=True, null=True
    )  # Field name made lowercase.
    dodajpracownikavisible = models.IntegerField(
        db_column="DodajPracownikaVisible", blank=True, null=True
    )  # Field name made lowercase.
    cofnijskanvisible = models.IntegerField(
        db_column="CofnijSkanVisible", blank=True, null=True
    )  # Field name made lowercase.
    zestawienieczynnoscinewvisible = models.IntegerField(
        db_column="ZestawienieCzynnosciNewVisible", blank=True, null=True
    )  # Field name made lowercase.
    visibilitylastdatechange = models.DateTimeField(
        db_column="VisibilityLastDateChange", blank=True, null=True
    )  # Field name made lowercase.
    image = models.CharField(
        db_column="Image",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "Uzytkownicy"


class Zlecenia(models.Model):
    indeks = models.IntegerField(
        db_column="Indeks", primary_key=True
    )  # Field name made lowercase.
    archiwum = models.IntegerField(
        db_column="Archiwum", blank=True, null=True
    )  # Field name made lowercase.
    data = models.DateTimeField(
        db_column="Data", blank=True, null=True
    )  # Field name made lowercase.
    datawejscia = models.DateTimeField(
        db_column="DataWejscia", blank=True, null=True
    )  # Field name made lowercase.
    datazakonczenia = models.DateTimeField(
        db_column="DataZakonczenia", blank=True, null=True
    )  # Field name made lowercase.
    del_field = models.IntegerField(
        db_column="Del", blank=True, null=True
    )  # Field name made lowercase. Field renamed because it was a Python reserved word.
    diler = models.CharField(
        db_column="Diler",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    firststanowisko = models.IntegerField(
        db_column="FirstStanowisko", blank=True, null=True
    )  # Field name made lowercase.
    hiden = models.IntegerField(
        db_column="Hiden", blank=True, null=True
    )  # Field name made lowercase.
    erridx = models.IntegerField(
        db_column="ErrIdx", blank=True, null=True
    )  # Field name made lowercase.
    klient = models.CharField(
        db_column="Klient",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    liczbaszklen = models.IntegerField(
        db_column="LiczbaSzklen", blank=True, null=True
    )  # Field name made lowercase.
    nipdilera = models.CharField(
        db_column="NipDilera",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    oscieznica = models.IntegerField(
        db_column="Oscieznica", blank=True, null=True
    )  # Field name made lowercase.
    pozycja = models.IntegerField(
        db_column="Pozycja", blank=True, null=True
    )  # Field name made lowercase.
    skanowanie = models.IntegerField(
        db_column="Skanowanie", blank=True, null=True
    )  # Field name made lowercase.
    skrzydlo = models.IntegerField(
        db_column="Skrzydlo", blank=True, null=True
    )  # Field name made lowercase.
    srcdoc = models.IntegerField(blank=True, null=True)
    stanowisko = models.IntegerField(
        db_column="Stanowisko", blank=True, null=True
    )  # Field name made lowercase.
    stanowiskopoprzednie = models.IntegerField(
        db_column="StanowiskoPoprzednie", blank=True, null=True
    )  # Field name made lowercase.
    sztuka = models.IntegerField(
        db_column="Sztuka", blank=True, null=True
    )  # Field name made lowercase.
    terminrealizacji = models.CharField(
        db_column="TerminRealizacji",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    zakonczone = models.IntegerField(
        db_column="Zakonczone", blank=True, null=True
    )  # Field name made lowercase.
    zlecenie = models.CharField(
        db_column="Zlecenie",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    zleceniedilera = models.CharField(
        db_column="ZlecenieDilera",
        max_length=50,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    dodopis = models.CharField(
        db_column="DodOpis",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    optym = models.IntegerField(blank=True, null=True)
    terminprodukcji = models.CharField(
        db_column="TerminProdukcji",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    optymalizacja = models.CharField(
        db_column="Optymalizacja",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    dbwhokna = models.IntegerField(
        db_column="DbWHOkna", blank=True, null=True
    )  # Field name made lowercase.
    kodbiura = models.CharField(
        db_column="KodBiura",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    optsrcdoc = models.IntegerField(
        db_column="OptSrcdoc", blank=True, null=True
    )  # Field name made lowercase.
    vip = models.IntegerField(
        db_column="Vip", blank=True, null=True
    )  # Field name made lowercase.
    obrazekosc = models.CharField(
        db_column="ObrazekOsc",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    obrazekskr = models.CharField(
        db_column="ObrazekSkr",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    referencja = models.CharField(
        db_column="Referencja",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    priorytet = models.IntegerField(
        db_column="Priorytet", blank=True, null=True
    )  # Field name made lowercase.
    iloscjedn = models.FloatField(
        db_column="IloscJedn", blank=True, null=True
    )  # Field name made lowercase.
    idx_typu = models.IntegerField(
        db_column="Idx_typu", blank=True, null=True
    )  # Field name made lowercase.
    typ = models.CharField(
        db_column="Typ",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    iloscjednpoz = models.FloatField(
        db_column="IloscJednPoz", blank=True, null=True
    )  # Field name made lowercase.
    pozycjalp = models.IntegerField(
        db_column="PozycjaLp", blank=True, null=True
    )  # Field name made lowercase.
    country = models.CharField(
        db_column="Country",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    framewidth = models.IntegerField(
        db_column="FrameWidth", blank=True, null=True
    )  # Field name made lowercase.
    frameheight = models.IntegerField(
        db_column="FrameHeight", blank=True, null=True
    )  # Field name made lowercase.
    sashwidth = models.IntegerField(
        db_column="SashWidth", blank=True, null=True
    )  # Field name made lowercase.
    sashheight = models.IntegerField(
        db_column="SashHeight", blank=True, null=True
    )  # Field name made lowercase.
    glazing = models.CharField(
        db_column="Glazing",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    glazingframe = models.CharField(
        db_column="GlazingFrame",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    glazingframecolor = models.CharField(
        db_column="GlazingFrameColor",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    color = models.CharField(
        db_column="Color",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    paczka = models.CharField(
        db_column="Paczka",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "Zlecenia"
