from django.db import models


class Skany(models.Model):
    indeks = models.IntegerField(
        db_column="Indeks", primary_key=True
    )
    archiwum = models.IntegerField(
        db_column="Archiwum", blank=True, null=True
    )
    data = models.DateTimeField(
        db_column="Data", blank=True, null=True
    )
    del_field = models.IntegerField(
        db_column="Del", blank=True, null=True
    )
    kodkreskowy = models.CharField(
        db_column="KodKreskowy",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    oscieznica = models.IntegerField(
        db_column="Oscieznica", blank=True, null=True
    )
    pozycja = models.IntegerField(
        db_column="Pozycja", blank=True, null=True
    )
    skrzydlo = models.IntegerField(
        db_column="Skrzydlo", blank=True, null=True
    )
    srcdoc = models.IntegerField(blank=True, null=True)
    stanowisko = models.IntegerField(
        db_column="Stanowisko", blank=True, null=True
    )
    sztuka = models.IntegerField(
        db_column="Sztuka", blank=True, null=True
    )
    uzytkownik = models.IntegerField(
        db_column="Uzytkownik", blank=True, null=True
    )
    zakonczony = models.IntegerField(
        db_column="Zakonczony", blank=True, null=True
    )
    czynnosc = models.IntegerField(
        db_column="Czynnosc", blank=True, null=True
    )
    dbwhokna = models.IntegerField(
        db_column="DbWHOkna", blank=True, null=True
    )
    guid = models.CharField(
        db_column="Guid",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    guidparent = models.CharField(
        db_column="GuidParent",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    status = models.IntegerField(
        db_column="Status", blank=True, null=True
    )
    typ = models.IntegerField(
        db_column="Typ", blank=True, null=True
    )
    typslupka = models.IntegerField(
        db_column="TypSlupka", blank=True, null=True
    )
    erridx = models.IntegerField(
        db_column="ErrIdx", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "Skany"


class SkanyVsZlecenia(models.Model):
    indeks = models.IntegerField(
        db_column="Indeks", primary_key=True
    )
    indeksskanu = models.IntegerField(
        db_column="IndeksSkanu", blank=True, null=True
    )
    indekszlecenia = models.IntegerField(
        db_column="IndeksZlecenia", blank=True, null=True
    )
    indeksdodatka = models.CharField(
        db_column="IndeksDodatka",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    duplicated = models.IntegerField(
        db_column="Duplicated", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "Skany_vs_Zlecenia"


class Stanowiska(models.Model):
    indeks = models.IntegerField(
        db_column="Indeks", primary_key=True
    )
    aktywny = models.IntegerField(
        db_column="Aktywny", blank=True, null=True
    )
    data = models.DateTimeField(
        db_column="Data", blank=True, null=True
    )
    del_field = models.IntegerField(
        db_column="Del", blank=True, null=True
    )
    drukujraport = models.CharField(
        db_column="DrukujRaport",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    liczbaporzadkowa = models.IntegerField(
        db_column="LiczbaPorzadkowa", blank=True, null=True
    )
    liniaprodukcyjna = models.IntegerField(
        db_column="LiniaProdukcyjna", blank=True, null=True
    )
    obslugastojakow = models.IntegerField(
        db_column="ObslugaStojakow", blank=True, null=True
    )
    opis = models.CharField(
        db_column="Opis",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    opisczynnosci = models.CharField(
        db_column="OpisCzynnosci",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    podstatusprzed = models.CharField(
        db_column="PodstatusPrzed",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    podstatuspo = models.CharField(
        db_column="PodstatusPo",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    raport = models.CharField(
        db_column="Raport",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    raportdodatki = models.CharField(
        db_column="RaportDodatki",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    rozwintabelke = models.IntegerField(
        db_column="RozwinTabelke", blank=True, null=True
    )
    skanowanie = models.IntegerField(
        db_column="Skanowanie", blank=True, null=True
    )
    stanowiskokoncowe = models.IntegerField(
        db_column="StanowiskoKoncowe", blank=True, null=True
    )
    wielkoscczcionki = models.IntegerField(
        db_column="WielkoscCzcionki", blank=True, null=True
    )
    zdejmowanie = models.IntegerField(
        db_column="Zdejmowanie", blank=True, null=True
    )
    zliczanie = models.IntegerField(
        db_column="Zliczanie", blank=True, null=True
    )
    zoom1 = models.IntegerField(
        db_column="Zoom1", blank=True, null=True
    )
    zoom2 = models.IntegerField(
        db_column="Zoom2", blank=True, null=True
    )
    proceduraskladowa = models.IntegerField(
        db_column="ProceduraSkladowa", blank=True, null=True
    )
    viewer = models.CharField(
        db_column="Viewer",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    czynnoscosc = models.IntegerField(
        db_column="CzynnoscOsc", blank=True, null=True
    )
    czynnoscskr = models.IntegerField(
        db_column="CzynnoscSkr", blank=True, null=True
    )
    czynnoscslr = models.IntegerField(
        db_column="CzynnoscSlr", blank=True, null=True
    )
    czynnoscsls = models.IntegerField(
        db_column="CzynnoscSls", blank=True, null=True
    )
    czynnoscszkl = models.IntegerField(
        db_column="CzynnoscSzkl", blank=True, null=True
    )
    obslugatransportu = models.IntegerField(
        db_column="ObslugaTransportu", blank=True, null=True
    )
    barcodeidx = models.IntegerField(
        db_column="BarcodeIdx", blank=True, null=True
    )
    barcodeprevidx = models.IntegerField(
        db_column="BarcodePrevIdx", blank=True, null=True
    )
    barcodenextidx = models.IntegerField(
        db_column="BarcodeNextIdx", blank=True, null=True
    )
    cursortimeout = models.IntegerField(
        db_column="CursorTimeout", blank=True, null=True
    )
    defaultevent = models.IntegerField(
        db_column="DefaultEvent", blank=True, null=True
    )
    tablefilter = models.IntegerField(
        db_column="TableFilter", blank=True, null=True
    )
    panelinfowidth = models.IntegerField(
        db_column="PanelInfoWidth", blank=True, null=True
    )
    printer = models.CharField(
        db_column="Printer",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    raportstojaki = models.CharField(
        db_column="RaportStojaki",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    zoomstands = models.IntegerField(
        db_column="ZoomStands", blank=True, null=True
    )
    middle = models.IntegerField(
        db_column="Middle", blank=True, null=True
    )
    middle_type = models.IntegerField(
        db_column="Middle_type", blank=True, null=True
    )
    obslugasektorow = models.IntegerField(
        db_column="ObslugaSektorow", blank=True, null=True
    )
    userdescription = models.CharField(
        db_column="UserDescription",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    userstatus = models.CharField(
        db_column="UserStatus",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    canhavedifferentip = models.CharField(
        db_column="CanHaveDifferentIP",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    qualitycontrolworkplace = models.CharField(
        db_column="QualityControlWorkplace",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    alvarchar = models.CharField(
        db_column="AlVARCHAR",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    altextrasworkplace = models.IntegerField(
        db_column="AlTEXTrasWorkplace", blank=True, null=True
    )
    allowglassscan = models.IntegerField(
        db_column="AllowGlassScan", blank=True, null=True
    )
    onlyoneworkeronthisworkplace = models.IntegerField(
        db_column="OnlyOneWorkerOnThisWorkplace", blank=True, null=True
    )
    altextrasdatecolumnname = models.CharField(
        db_column="AlTEXTrasDateColumnName",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    hidelaborbutton = models.IntegerField(
        db_column="HideLaborButton", blank=True, null=True
    )
    importpackagestoszybyxls = models.IntegerField(
        db_column="ImportPackagesToSzybyXLS", blank=True, null=True
    )
    hidetableinpackagesloading = models.IntegerField(
        db_column="HideTableInPackagesLoading", blank=True, null=True
    )
    altcuttingworkplace = models.IntegerField(
        db_column="AltCuttingWorkplace", blank=True, null=True
    )
    mobile = models.IntegerField(
        db_column="Mobile", blank=True, null=True
    )
    markwhentransportispacked = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Stanowiska"


class Uzytkownicy(models.Model):
    indeks = models.IntegerField(
        db_column="Indeks", primary_key=True
    )
    aktywny = models.IntegerField(
        db_column="Aktywny", blank=True, null=True
    )
    data = models.DateTimeField(
        db_column="Data", blank=True, null=True
    )
    dealer = models.CharField(
        db_column="Dealer",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    del_field = models.IntegerField(
        db_column="Del", blank=True, null=True
    )
    haslo = models.CharField(
        db_column="Haslo",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    imie = models.CharField(
        db_column="Imie",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    login = models.CharField(
        db_column="Login",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    nazwa = models.CharField(
        db_column="Nazwa",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    nazwisko = models.CharField(
        db_column="Nazwisko",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    nip = models.CharField(
        db_column="Nip",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    uprawnienia = models.IntegerField(
        db_column="Uprawnienia", blank=True, null=True
    )
    usr = models.IntegerField(
        db_column="Usr", blank=True, null=True
    )
    uwagi = models.CharField(
        db_column="Uwagi",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    stawkadzienna = models.IntegerField(
        db_column="StawkaDzienna", blank=True, null=True
    )
    barcodeidx = models.IntegerField(
        db_column="BarcodeIdx", blank=True, null=True
    )
    language = models.CharField(
        db_column="Language",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    grupaplacowa = models.IntegerField(
        db_column="GrupaPlacowa", blank=True, null=True
    )
    tworzenieartykulow = models.IntegerField(
        db_column="TworzenieArtykulow", blank=True, null=True
    )
    email = models.CharField(
        db_column="Email",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    zestawieniezlecennaprodukcjivisible = models.IntegerField(
        db_column="ZestawienieZlecenNaProdukcjiVisible", blank=True, null=True
    )
    zawartoscstojakowvisible = models.IntegerField(
        db_column="ZawartoscStojakowVisible", blank=True, null=True
    )
    zawartoscsamochodowvisible = models.IntegerField(
        db_column="ZawartoscSamochodowVisible", blank=True, null=True
    )
    zawartoscsektorowvisible = models.IntegerField(
        db_column="ZawartoscSektorowVisible", blank=True, null=True
    )
    zawartoscsektorowszkleniavisible = models.IntegerField(
        db_column="ZawartoscSektorowSzkleniaVisible", blank=True, null=True
    )
    zestawienieczynnoscivisible = models.IntegerField(
        db_column="ZestawienieCzynnosciVisible", blank=True, null=True
    )
    zestawienieodpowiedzinapytaniavisible = models.IntegerField(
        db_column="ZestawienieOdpowiedziNaPytaniaVisible", blank=True, null=True
    )
    zestawienierobociznyvisible = models.IntegerField(
        db_column="ZestawienieRobociznyVisible", blank=True, null=True
    )
    zestawieniebledowkomunikatownotatekvisible = models.IntegerField(
        db_column="ZestawienieBledowKomunikatowNotatekVisible", blank=True, null=True
    )
    eksportwykonanychoscieznicvisible = models.IntegerField(
        db_column="EksportWykonanychOscieznicVisible", blank=True, null=True
    )
    posteprealizacjivisible = models.IntegerField(
        db_column="PostepRealizacjiVisible", blank=True, null=True
    )
    dodajpracownikavisible = models.IntegerField(
        db_column="DodajPracownikaVisible", blank=True, null=True
    )
    cofnijskanvisible = models.IntegerField(
        db_column="CofnijSkanVisible", blank=True, null=True
    )
    zestawienieczynnoscinewvisible = models.IntegerField(
        db_column="ZestawienieCzynnosciNewVisible", blank=True, null=True
    )
    visibilitylastdatechange = models.DateTimeField(
        db_column="VisibilityLastDateChange", blank=True, null=True
    )
    image = models.CharField(
        db_column="Image",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "Uzytkownicy"


class Zlecenia(models.Model):
    indeks = models.IntegerField(
        db_column="Indeks", primary_key=True
    )
    archiwum = models.IntegerField(
        db_column="Archiwum", blank=True, null=True
    )
    data = models.DateTimeField(
        db_column="Data", blank=True, null=True
    )
    datawejscia = models.DateTimeField(
        db_column="DataWejscia", blank=True, null=True
    )
    datazakonczenia = models.DateTimeField(
        db_column="DataZakonczenia", blank=True, null=True
    )
    del_field = models.IntegerField(
        db_column="Del", blank=True, null=True
    )
    diler = models.CharField(
        db_column="Diler",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    firststanowisko = models.IntegerField(
        db_column="FirstStanowisko", blank=True, null=True
    )
    hiden = models.IntegerField(
        db_column="Hiden", blank=True, null=True
    )
    erridx = models.IntegerField(
        db_column="ErrIdx", blank=True, null=True
    )
    klient = models.CharField(
        db_column="Klient",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    liczbaszklen = models.IntegerField(
        db_column="LiczbaSzklen", blank=True, null=True
    )
    nipdilera = models.CharField(
        db_column="NipDilera",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    oscieznica = models.IntegerField(
        db_column="Oscieznica", blank=True, null=True
    )
    pozycja = models.IntegerField(
        db_column="Pozycja", blank=True, null=True
    )
    skanowanie = models.IntegerField(
        db_column="Skanowanie", blank=True, null=True
    )
    skrzydlo = models.IntegerField(
        db_column="Skrzydlo", blank=True, null=True
    )
    srcdoc = models.IntegerField(blank=True, null=True)
    stanowisko = models.IntegerField(
        db_column="Stanowisko", blank=True, null=True
    )
    stanowiskopoprzednie = models.IntegerField(
        db_column="StanowiskoPoprzednie", blank=True, null=True
    )
    sztuka = models.IntegerField(
        db_column="Sztuka", blank=True, null=True
    )
    terminrealizacji = models.CharField(
        db_column="TerminRealizacji",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    zakonczone = models.IntegerField(
        db_column="Zakonczone", blank=True, null=True
    )
    zlecenie = models.CharField(
        db_column="Zlecenie",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    zleceniedilera = models.CharField(
        db_column="ZlecenieDilera",
        max_length=50,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    dodopis = models.CharField(
        db_column="DodOpis",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    optym = models.IntegerField(blank=True, null=True)
    terminprodukcji = models.CharField(
        db_column="TerminProdukcji",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    optymalizacja = models.CharField(
        db_column="Optymalizacja",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    dbwhokna = models.IntegerField(
        db_column="DbWHOkna", blank=True, null=True
    )
    kodbiura = models.CharField(
        db_column="KodBiura",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    optsrcdoc = models.IntegerField(
        db_column="OptSrcdoc", blank=True, null=True
    )
    vip = models.IntegerField(
        db_column="Vip", blank=True, null=True
    )
    obrazekosc = models.CharField(
        db_column="ObrazekOsc",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    obrazekskr = models.CharField(
        db_column="ObrazekSkr",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    referencja = models.CharField(
        db_column="Referencja",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    priorytet = models.IntegerField(
        db_column="Priorytet", blank=True, null=True
    )
    iloscjedn = models.FloatField(
        db_column="IloscJedn", blank=True, null=True
    )
    idx_typu = models.IntegerField(
        db_column="Idx_typu", blank=True, null=True
    )
    typ = models.CharField(
        db_column="Typ",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    iloscjednpoz = models.FloatField(
        db_column="IloscJednPoz", blank=True, null=True
    )
    pozycjalp = models.IntegerField(
        db_column="PozycjaLp", blank=True, null=True
    )
    country = models.CharField(
        db_column="Country",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    framewidth = models.IntegerField(
        db_column="FrameWidth", blank=True, null=True
    )
    frameheight = models.IntegerField(
        db_column="FrameHeight", blank=True, null=True
    )
    sashwidth = models.IntegerField(
        db_column="SashWidth", blank=True, null=True
    )
    sashheight = models.IntegerField(
        db_column="SashHeight", blank=True, null=True
    )
    glazing = models.CharField(
        db_column="Glazing",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    glazingframe = models.CharField(
        db_column="GlazingFrame",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    glazingframecolor = models.CharField(
        db_column="GlazingFrameColor",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    color = models.CharField(
        db_column="Color",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    paczka = models.CharField(
        db_column="Paczka",
        max_length=250,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "Zlecenia"
