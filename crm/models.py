from django.db import models
import uuid


ConsignemntStatusChoices = [
    ["created","created"],
    ["in-transit","in-transit"],
    ["reached","reached"],
    ["out-for-delivery","out-for-delivery"],
    ["delivered","delivered"],
    ["attempted","attempted"],
    ["returned","returned"],
    ["undelivered","undelivered"]
]

ConsignmentModeChoices = [
    ["forward","forward"],
    ["reverse","reverse"]
]



class Vendor(models.Model):
    '''
    Logistic vendors
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    phone = models.CharField(default=0, max_length=10)
    pin = models.IntegerField(default=0)
    createdDate = models.DateTimeField(auto_now_add=True)
    createdBy = models.IntegerField()
    modifiedDate = models.DateTimeField(auto_now=True)
    modifiededBy = models.IntegerField()
    deletedOn = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"
    
    # class Meta:
    #     verbose_name = "User"
    #     verbose_name_plural = "Users"

    class Meta:
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"


class VendorDetails(models.Model):
    '''
    Logistic partner details
    CoLoader and ChannelPartner

    Local Config is preferred over Global Config
    '''
    vendorTypeChoices = [
        ["CoLoader","CoLoader"],
        ["ChannelPartner","ChannelPartner"],
    ]


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Vendor Name")
    address = models.CharField(max_length=200, verbose_name="Address", blank=True, null=True)
    vendorType = models.CharField(max_length=100, choices=vendorTypeChoices, verbose_name="Vendor Type")
    email = models.EmailField(max_length=254, verbose_name="Email", blank=True, null=True)
    phone = models.CharField(default=0, max_length=10, verbose_name="Phone")
    pincode = models.CharField(max_length=7, verbose_name="Pincode", blank=True, null=True)
    pin = models.IntegerField(default=0, verbose_name="pin", blank=True, null=True)
    odaCharge = models.IntegerField(default=0, verbose_name="ODA Charge", blank=True, null=True)
    fixedCharge = models.IntegerField(default=0, verbose_name="Fixed Charge", blank=True, null=True)
    miscCharge = models.IntegerField(default=0, verbose_name="Misc Charge", blank=True, null=True)
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    createdBy = models.CharField(max_length=100, verbose_name="Created By", blank=True, null=True)
    modifiedDate = models.DateTimeField(auto_now=True, verbose_name="Modified Date")
    modifiedBy = models.CharField(max_length=100, verbose_name="Modified By", blank=True, null=True)
    deletedOn = models.DateTimeField(auto_now=True, verbose_name="Deleted On")

    def __str__(self):
        return f"{self.name}"
    
    # class Meta:
    #     verbose_name = "Vendor"
    #     verbose_name_plural = "Vendors"

    class Meta:
        verbose_name = "Partner"
        verbose_name_plural = "Partner"



class VendorLocation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(VendorDetails, on_delete=models.CASCADE)
    location = models.ForeignKey("Location", on_delete=models.CASCADE, related_name="vendorLocation")

    createdDate = models.DateTimeField(auto_now_add=True)
    createdBy = models.CharField(max_length=100, null=True, blank=True, default="System")
    modifiedDate = models.DateTimeField(auto_now=True)
    modifiedBy = models.CharField(max_length=100, null=True, blank=True, default="System")

    def __str__(self):
        return f"{self.vendor} - {self.location}"
    
    class Meta:
        verbose_name = "Location Mapping"
        verbose_name_plural = "Location Mapping"

class Users(models.Model):
    '''
    Airtel Details and Admin Details (Logiswift)
    '''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    phone = models.CharField(default=0, max_length=10)
    pincode = models.CharField(max_length=7)
    pin = models.IntegerField(default=0)
    createdDate = models.DateTimeField(auto_now_add=True)
    createdBy = models.CharField(max_length=100)
    modifiedDate = models.DateTimeField(auto_now=True)
    modifiedBy = models.CharField(max_length=100)
    deletedOn = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.pincode}"
    
    # class Meta:
    #     verbose_name = "Account"
    #     verbose_name_plural = "Accounts"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"




'''
Create a Sub-Location mapping Model
'''

class Location(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=100)
    sublocation = models.CharField(max_length=100, blank=True, null=True)
    # pincode = models.CharField(max_length=7)
    state = models.CharField(max_length=100, blank=True, null=True)
    rate = models.IntegerField(default=0, blank=True, null=True)
    location_type = models.CharField(max_length=100, verbose_name="Location Type",
        choices=[
            ("ODA","ODA"),
            ("Normal","Normal")
        ], default="Normal")
    enabled = models.BooleanField(default=True)
    # tat = models.IntegerField(blank=True, null=True, default=None)
    createdDate = models.DateTimeField(auto_now_add=True)
    createdBy = models.CharField(max_length=100, null=True, blank=True)
    modifiedDate = models.DateTimeField(auto_now=True, null=True, blank=True)
    modifiedBy = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        if self.sublocation:
            return f"{self.sublocation} - {self.location}"
        return f"{self.location}"

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"





class ConsigneeConsigner(models.Model):
    # If location mapping id exisis
    # then used that id as location and destination as sublocation
    # else destination as location
    # Location_type -> if sub_loacation then ODA else normal
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Name")
    address = models.CharField(max_length=200, verbose_name="Address")
    destination = models.CharField(max_length=100, verbose_name="Destination")
    locationMappingId = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="locationMappingId", null=True, blank=True, verbose_name="Location")
    # locationMappingId = models.ManyToManyField(Location, related_name="locationMappingId", blank=True, verbose_name="Location")
    state = models.CharField(max_length=50, verbose_name="State", null=True, blank=True)
    email = models.EmailField(max_length=254, blank=True, null=True, verbose_name="Email")
    pincode = models.CharField(max_length=7, verbose_name="Pincode", null=True, blank=True)
    phone = models.CharField(default=None, max_length=10, verbose_name="Phone", null=True, blank=True)
    tat = models.IntegerField(default=None, verbose_name="Tat", null=True, blank=True)
    
    rate = models.IntegerField(default=0, verbose_name="Rate", null=True, blank=True)
    odaCharge = models.IntegerField(default=0, verbose_name="ODA Charges", null=True, blank=True)
    
    location_type = models.CharField(max_length=100, verbose_name="Location Type",
        choices=[
            ("ODA","ODA"),
            ("Normal","Normal")
        ], default="Normal")
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_id", default=1, verbose_name="Users")
    deleted = models.BooleanField(default=False)

    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    createdBy = models.CharField(max_length=100, default=0, verbose_name="Created By")
    modifiedDate = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Modified Date")
    modifiedBy = models.CharField(max_length=100, default=0, verbose_name="Modified By")
    deletedOn = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Deleted On")

    def __str__(self):
        return f"{self.name}"
    
    def soft_delete(self):
        self.deleted = True
        return self.save()
    
    class Meta:
        verbose_name = "Distributor"
        verbose_name_plural = "Distributors"


class Consignment(models.Model):
    id = models.AutoField(primary_key=True)
    lr = models.CharField(unique=True, verbose_name="LR No.", max_length=100, blank=True, null=True)
    # consignmentDate = models.DateField(verbose_name="LR Date", null=True, blank=True, default=None)
    consignee_id = models.ForeignKey(ConsigneeConsigner, on_delete=models.CASCADE, related_name="consignee_id", verbose_name="Sender")
    consigner_id = models.ForeignKey(ConsigneeConsigner, on_delete=models.CASCADE, related_name="consigner_id", verbose_name="Reciever")
    quantity = models.IntegerField(default=0, verbose_name="Quantity")
    weight = models.DecimalField(default=0, max_digits=7, decimal_places=2, verbose_name="Weight in kgs")
    # weight = models.IntegerField(default=0, verbose_name="Weight in kgs")
    vendor_id = models.ForeignKey(VendorDetails, on_delete=models.CASCADE, related_name="vendor_id", verbose_name="Channel Partner", null=True, blank=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="consignment_user_id", verbose_name="User", default=1)
    status = models.CharField(max_length=100, choices=ConsignemntStatusChoices, default="created", verbose_name="Consignment Status")
    pod = models.FileField(upload_to='pod/', blank=True, null=True, verbose_name="Proof of Delivery")
    mode = models.CharField(max_length=100, choices=ConsignmentModeChoices, default="forward", verbose_name="Consignment Mode")
    reverseDocketNo = models.CharField(default=0, max_length=100, verbose_name="Reverse Docket Number", blank=True, null=True)
    remarks = models.CharField(max_length=500, verbose_name="Remarks", blank=True, null=True)
    
    expectedDeliveryDate = models.DateField(default=None, null=True, blank=True)
    tatstatus = models.CharField(max_length=10, blank=True, null=True, choices=[
        ["passed", "passed"],
        ["failed", "failed"]], default=None)
    variance = models.IntegerField(null=True, blank=True, default=None)
    
    
    # additional attributes
    delayed = models.BooleanField(default=False)
    delayedReason = models.TextField(blank=True, null=True, default=None)
    notified = models.BooleanField(default=False)
    notifiedDate = models.DateField(null=True, blank=True, default=None)
    additionalCharges = models.DecimalField(null=True, blank=True, default=0, max_digits=10, decimal_places=2)
    additionalChargesReason = models.TextField(null=True, blank=True, default=None)
    
    
    # location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, related_name="consignment_location", verbose_name="Location", default=None, null=True, blank=True)

    # distributor_ids = models.CharField(max_length=200, default=None, null=True, blank=True)
    # cp_id = models.CharField(max_length=100, default=None, null=True, blank=True)
    # location_name = models.CharField(max_length=100, default=None, null=True, blank=True)

    # createdDate = models.DateField(auto_now_add=False, verbose_name="LR Date")
    lrDate = models.DateField(auto_now_add=False, verbose_name="LR Date")
    createdBy = models.CharField(max_length=100, verbose_name="Created By")
    deliveryDate = models.DateField(verbose_name="Delivery Date", null=True, blank=True, default=None)
    modifiedDate = models.DateTimeField(auto_now=True, verbose_name="Modified Date")
    modifiedBy = models.CharField(max_length=100, verbose_name="Modified By")
    deletedOn = models.DateTimeField(auto_now=True, verbose_name="Deleted On")


    def __str__(self):
        return f"{self.lr}"
    
    
    

    class Meta:
        verbose_name = "Consignment"
        verbose_name_plural = "Consignments"


class PublicHolidays(models.Model):
    id = models.AutoField(primary_key=True)
    
    date = models.DateField()
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.description
    
    class Meta:
        verbose_name = "Public Holiday"
        verbose_name_plural = "Public Holidays"
    
    

class Billings(models.Model):
    id = models.AutoField(primary_key=True)
    
    lr = models.ForeignKey(Consignment, on_delete=models.CASCADE, related_name="consignment_billings")
    
    tatstatus = models.CharField(max_length=10, blank=True, null=True, choices=[
        ["passed", "passed"],
        ["failed", "failed"]], default=None)
    variance = models.IntegerField(null=True, blank=True, default=None)
    
    consigneeId = models.IntegerField(null=True, blank=True, default=None)
    consignerId = models.IntegerField(null=True, blank=True, default=None)
    locationId = models.IntegerField(null=True, blank=True, default=None)
    locationName = models.CharField(max_length=300, null=True, blank=True, default=None)
    consigneeName = models.CharField(max_length=300, null=True, blank=True, default=None)
    consignerName = models.CharField(max_length=300, null=True, blank=True, default=None)
    
    
    chargeableWeight = models.IntegerField(default=0)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    additionalCharge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    odaCharge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    cp_chargeableWeight = models.IntegerField(default=0)
    cp_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cp_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cp_additionalCharge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    cp_odaCharge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    cp_totalAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    vehicleCharge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    miscCharge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    miscRemark = models.TextField(default=None, null=True, blank=True)
    labourCharge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    officeExpense = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, null=True, blank=True, default=None)
    updated_by = models.CharField(max_length=255, null=True, blank=True, default=None)

    def __str__(self):
        return f"Billing {self.id}"
