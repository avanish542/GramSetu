from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from apps.accounts.models import User, UserRole
from apps.village.models import Village, Ward, VillageInfo, VillageCondition, RelatedPanchayat
from apps.development.models import DevelopmentProject, ProjectCategory, ProjectStatus, ProjectExpense, ProjectTimeline
from apps.complaints.models import Complaint, ComplaintCategory, ComplaintPriority, ComplaintStatus, ComplaintUpdate
from apps.services.models import PanchayatService, ServiceRequirement
from apps.applications.models import ServiceApplication, ApplicationStatus
from apps.schemes.models import GovernmentScheme, SchemeCategory
from apps.notices.models import Notice, NoticeCategory
from apps.gallery.models import GalleryItem, GalleryCategory
from apps.infrastructure.models import InfrastructureItem, InfraCategory, InfraStatus
from apps.feedback.models import ProjectFeedback
from apps.notifications.models import InAppNotification, NotificationType
from apps.audit.models import AuditLog

class Command(BaseCommand):
    help = "Seeds database with complete, realistic demo data for Tenuhari (Shukla) Gram Panchayat, Sahjanwa, Gorakhpur."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting GramSetu V2 demo data seeding for Tenuhari (Shukla)..."))

        # 1. Primary Village & Wards
        village, _ = Village.objects.get_or_create(
            name="Tenuhari (Shukla)",
            defaults={
                "gram_panchayat": "Tenuhari (Shukla) Gram Panchayat",
                "block": "Sahjanwa",
                "district": "Gorakhpur",
                "state": "Uttar Pradesh",
                "pincode": "273209",
                "population": 5800,
                "households": 950,
                "total_wards": 6,
                "history": "Tenuhari (Shukla) is a vibrant Gram Panchayat located in Sahjanwa Tehsil, Gorakhpur District, Uttar Pradesh (PIN 273209). Known for its agricultural heritage, local enterprise, and active citizen participation under Sarpanch MOHANLAL."
            }
        )
        # Update fields in case village existed previously with old name
        village.gram_panchayat = "Tenuhari (Shukla) Gram Panchayat"
        village.block = "Sahjanwa"
        village.district = "Gorakhpur"
        village.state = "Uttar Pradesh"
        village.pincode = "273209"
        village.save()

        wards_data = [
            (1, "Tenuhari Khas", "Shri Ram Lal", "9876543210", 1050),
            (2, "Shukla Mohalla", "Smt. Sunita Devi", "9876543211", 980),
            (3, "School Tola", "Shri Vikram Singh", "9876543212", 950),
            (4, "Sahjanwa Marg", "Shri Rajesh Kumar", "9876543213", 920),
            (5, "Panchayat Bhawan Tola", "Smt. Maya Verma", "9876543214", 960),
            (6, "Purab Tola", "Shri Suresh Chandra", "9876543215", 940),
        ]
        wards = []
        for w_num, w_name, rep_name, rep_phone, pop in wards_data:
            ward, _ = Ward.objects.update_or_create(
                village=village,
                ward_number=w_num,
                defaults={
                    "ward_name": w_name,
                    "representative_name": rep_name,
                    "representative_phone": rep_phone,
                    "population": pop
                }
            )
            wards.append(ward)

        VillageInfo.objects.update_or_create(
            village=village,
            defaults={
                "schools_count": 3,
                "health_centers_count": 1,
                "water_facilities_overview": "Jal Jeevan Mission piped water network expansion and community deep borewell handpumps across all wards.",
                "electricity_coverage_percent": 97.50,
                "waste_management_overview": "Door-to-door waste collection bins and organic composting pits managed by Gram Panchayat.",
                "panchayat_office_address": "Gram Panchayat Bhawan, Tenuhari (Shukla), Sahjanwa, Gorakhpur, UP - 273209",
                "panchayat_contact_email": "admin@tenuharipanchayat.in",
                "panchayat_contact_phone": "+91 551 2345678"
            }
        )

        # 1b. Seed Village Conditions (Part 4 & STEP 4)
        conditions_data = [
            ('Roads', 'MODERATE', 'Main connectivity road is paved; narrow internal lanes need paver block work. [Sample Assessment]', 'Ward 4 paver block work planned', 'Demo Data / Sample Assessment', False),
            ('Drainage', 'NEEDS_ATTENTION', 'Covered drains exist in Ward 1 & 2; monsoon overflow requires widening in Ward 4. [Sample Assessment]', 'Clearing scheduled before monsoon', 'Demo Data / Sample Assessment', False),
            ('Drinking Water', 'GOOD', 'Piped water supply network under Jal Jeevan Mission and functional handpumps. [Sample Assessment]', 'Coverage expanding across all wards', 'Demo Data / Sample Assessment', False),
            ('Electricity', 'GOOD', '97.5% household grid coverage with dedicated 250kVA transformer. [Sample Assessment]', 'Transformer upgraded recently', 'Demo Data / Sample Assessment', False),
            ('Street Lighting', 'GOOD', '80+ solar LED street lights installed across key intersections and lanes. [Sample Assessment]', 'Routine maintenance handled by local operator', 'Demo Data / Sample Assessment', False),
            ('Schools', 'GOOD', 'Primary school with smart classroom equipment and drinking water facilities. [Sample Assessment]', 'Classroom repairs completed', 'Demo Data / Sample Assessment', False),
            ('Health Facilities', 'MODERATE', 'Health sub-centre operational; primary health center visits scheduled weekly. [Sample Assessment]', 'Sub-centre extension in progress', 'Demo Data / Sample Assessment', False),
            ('Sanitation', 'MODERATE', 'Regular sanitization drives and swachhata awareness campaigns. [Sample Assessment]', 'Gram Sabha cleanliness drive organized monthly', 'Demo Data / Sample Assessment', False),
            ('Waste Management', 'NEEDS_ATTENTION', 'Solid waste segregation unit under construction near Sahjanwa Marg. [Sample Assessment]', 'Composting pit construction underway', 'Demo Data / Sample Assessment', False),
            ('Internet/Digital Connectivity', 'MODERATE', '4G mobile coverage across all wards; Panchayat CSC digital kiosk operational. [Sample Assessment]', 'Free Wi-Fi at Panchayat Bhawan', 'Demo Data / Sample Assessment', False),
            ('Agriculture', 'GOOD', 'Tube well irrigation network and subsidized solar pump adoption. [Sample Assessment]', 'Solar pump subsidy applications processed', 'Demo Data / Sample Assessment', False),
            ('Transportation', 'MODERATE', 'Regular shared tempo/auto connection to Sahjanwa Tehsil and Gorakhpur city. [Sample Assessment]', 'Connecting road paving underway', 'Demo Data / Sample Assessment', False),
            ('Public Buildings', 'GOOD', 'Gram Panchayat Bhawan equipped with computer lab and meeting room. [Sample Assessment]', 'Administrative CSC functional', 'Demo Data / Sample Assessment', False),
            ('Water Bodies', 'UNKNOWN', 'Village pond condition assessment unverified; survey requested. [Unverified Status]', 'Requires field survey by Irrigation department', 'Unverified / Field Survey Pending', False),
        ]
        for cat, status, desc, rem, src, ver in conditions_data:
            VillageCondition.objects.update_or_create(
                village=village,
                category=cat,
                defaults={
                    "condition_status": status,
                    "description": desc,
                    "remarks": rem,
                    "source": src,
                    "verified": ver
                }
            )

        # 1c. Seed Related Panchayats / Sahjanwa Block Locations (Part 5)
        sahjanwa_gps = [
            ("Tenuhari (Shukla)", "PRIMARY_GP", 0.0, "Primary Gram Panchayat platform location"),
            ("Tenuhari Khas", "REVENUE_VILLAGE", 0.5, "Revenue village under Tenuhari Gram Panchayat"),
            ("Shukla Tola", "REVENUE_VILLAGE", 0.8, "Revenue hamlet under Tenuhari Gram Panchayat"),
            ("Bhiti Rawot", "SAHJANWA_GP", 3.5, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Mahuapar", "SAHJANWA_GP", 4.2, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Sihapar", "SAHJANWA_GP", 5.0, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Hardi", "SAHJANWA_GP", 4.8, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Piparhema", "SAHJANWA_GP", 6.1, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Gidha", "SAHJANWA_GP", 5.5, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Sahijana", "SAHJANWA_GP", 6.8, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Khajuri", "SAHJANWA_GP", 7.2, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Rankolee", "SAHJANWA_GP", 8.0, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Raghunathpur", "SAHJANWA_GP", 6.5, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Ramnagar", "SAHJANWA_GP", 7.5, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Rampur Garthauli", "SAHJANWA_GP", 8.2, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Budhat", "SAHJANWA_GP", 9.0, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Bharsar", "SAHJANWA_GP", 9.5, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Anantpur", "SAHJANWA_GP", 10.0, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Deoria", "SAHJANWA_GP", 10.5, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Gangtahi", "SAHJANWA_GP", 11.0, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Baidauli", "SAHJANWA_GP", 11.5, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Baijalpur", "SAHJANWA_GP", 12.0, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Bhaluwa", "SAHJANWA_GP", 12.5, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Harpur", "SAHJANWA_GP", 13.0, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Kodri Kala", "SAHJANWA_GP", 13.5, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Khiridand", "SAHJANWA_GP", 14.0, "Gram Panchayat in Sahjanwa Block, Gorakhpur"),
            ("Daftari Location", "SAHJANWA_GP", 7.8, "Gram Panchayat location in Sahjanwa area"),
            ("Jura Kodri Location", "SAHJANWA_GP", 12.2, "Gram Panchayat location in Sahjanwa area"),
        ]
        created_rel_gps = {}
        for gp_name, gp_cat, dist_km, notes in sahjanwa_gps:
            rp, _ = RelatedPanchayat.objects.update_or_create(
                name=gp_name,
                defaults={
                    "category": gp_cat,
                    "tehsil": "Sahjanwa",
                    "district": "Gorakhpur",
                    "state": "Uttar Pradesh",
                    "distance_km": dist_km,
                    "notes": notes
                }
            )
            created_rel_gps[gp_name] = rp

        # Seed condition records for sample related locations
        if "Bhiti Rawot" in created_rel_gps:
            VillageCondition.objects.update_or_create(
                related_panchayat=created_rel_gps["Bhiti Rawot"],
                category='Roads',
                defaults={'condition_status': 'GOOD', 'description': 'Main approach road paved. [Sample Data]', 'source': 'Demo Data / Sample Assessment'}
            )
            VillageCondition.objects.update_or_create(
                related_panchayat=created_rel_gps["Bhiti Rawot"],
                category='Drainage',
                defaults={'condition_status': 'MODERATE', 'description': 'Open drain network. [Sample Data]', 'source': 'Demo Data / Sample Assessment'}
            )

        if "Mahuapar" in created_rel_gps:
            VillageCondition.objects.update_or_create(
                related_panchayat=created_rel_gps["Mahuapar"],
                category='Drinking Water',
                defaults={'condition_status': 'GOOD', 'description': 'Handpumps & Jal Jeevan line. [Sample Data]', 'source': 'Demo Data / Sample Assessment'}
            )
            VillageCondition.objects.update_or_create(
                related_panchayat=created_rel_gps["Mahuapar"],
                category='Electricity',
                defaults={'condition_status': 'GOOD', 'description': '24x7 rural feeder line. [Sample Data]', 'source': 'Demo Data / Sample Assessment'}
            )

        if "Gidha" in created_rel_gps:
            VillageCondition.objects.update_or_create(
                related_panchayat=created_rel_gps["Gidha"],
                category='Roads',
                defaults={'condition_status': 'NEEDS_ATTENTION', 'description': 'Pothole repair required. [Sample Data]', 'source': 'Demo Data / Sample Assessment'}
            )


        # 2. Users & Roles
        super_admin, _ = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@gramsetu.in",
                "first_name": "System",
                "last_name": "Administrator",
                "role": UserRole.SUPER_ADMIN,
                "is_staff": True,
                "is_superuser": True,
                "is_verified": True,
                "village": village
            }
        )
        super_admin.set_password("admin12345")
        super_admin.save()

        panchayat_admin, _ = User.objects.get_or_create(
            username="sarpanch",
            defaults={
                "email": "sarpanch@tenuharipanchayat.in",
                "first_name": "MOHANLAL",
                "last_name": "(Sarpanch)",
                "role": UserRole.PANCHAYAT_ADMIN,
                "is_staff": True,
                "is_verified": True,
                "village": village,
                "phone": "9812345678"
            }
        )
        panchayat_admin.first_name = "MOHANLAL"
        panchayat_admin.last_name = "(Sarpanch)"
        panchayat_admin.email = "sarpanch@tenuharipanchayat.in"
        panchayat_admin.set_password("admin12345")
        panchayat_admin.save()

        villagers_data = [
            ("ramesh", "ramesh@example.com", "Ramesh", "Kumar", "9988776655", wards[0]),
            ("sita", "sita@example.com", "Sita", "Devi", "9988776654", wards[1]),
            ("amit", "amit@example.com", "Amit", "Sharma", "9988776653", wards[2]),
            ("priya", "priya@example.com", "Priya", "Singh", "9988776652", wards[3]),
        ]
        villagers = []
        for uname, uemail, fname, lname, phone, ward in villagers_data:
            user, _ = User.objects.get_or_create(
                username=uname,
                defaults={
                    "email": uemail,
                    "first_name": fname,
                    "last_name": lname,
                    "phone": phone,
                    "role": UserRole.VILLAGER,
                    "village": village,
                    "ward": ward,
                    "is_verified": True
                }
            )
            user.village = village
            user.set_password("pass12345")
            user.save()
            villagers.append(user)

        # 3. Project Categories
        categories_data = [
            ("Roads", "roads", "Concrete road construction and paving", "truck"),
            ("Drainage / Gutters", "drainage", "Covered storm water and sewage drains", "water"),
            ("Water Supply", "water-supply", "Piped drinking water, hand pumps, and tanks", "droplet"),
            ("Street Lights", "street-lights", "Solar and LED street lighting network", "sun"),
            ("Schools", "schools", "Primary school classrooms and digital labs", "academic-cap"),
            ("Health Facilities", "health-facilities", "Primary Health Centre and maternity care", "heart"),
            ("Parks / Playgrounds", "parks", "Public green parks and sports ground", "tree"),
            ("Waste Management", "waste-management", "Composting and waste collection units", "trash"),
            ("Electricity", "electricity", "Transformer upgrades and power grid expansion", "bolt"),
            ("Other", "other", "Community hall and miscellaneous infrastructure", "building"),
        ]
        cat_map = {}
        for name, slug, desc, icon in categories_data:
            cat, _ = ProjectCategory.objects.get_or_create(slug=slug, defaults={"name": name, "description": desc, "icon": icon})
            cat_map[slug] = cat

        # 4. 20+ Development Projects (Centered at Sahjanwa/Tenuhari ~26.7725, 83.1783)
        projects_data = [
            ("PRJ-2026-0001", "Sahjanwa Marg CC Road Paving", "roads", "Construction of 2.2 km concrete road connecting Tenuhari to Sahjanwa main road. [Sample Demo Data]", "Sahjanwa Marg, Ward 4", wards[3], 26.7735, 83.1795, 1500000, 1500000, 1200000, "15th Finance Commission", ProjectStatus.IN_PROGRESS, 80),
            ("PRJ-2026-0002", "Ward 1 Tenuhari Covered Drainage Network", "drainage", "Construction of RCC covered drain along Tenuhari Khas main street. [Sample Demo Data]", "Tenuhari Khas", wards[0], 26.7710, 83.1770, 850000, 850000, 850000, "State Rural Dev Fund", ProjectStatus.COMPLETED, 100),
            ("PRJ-2026-0003", "Solar LED Street Light Installation Phase 2", "street-lights", "Installation of 80 solar LED streetlights across all wards. [Sample Demo Data]", "All Wards", wards[1], 26.7728, 83.1788, 600000, 600000, 450000, "Clean Energy Grant", ProjectStatus.IN_PROGRESS, 75),
            ("PRJ-2026-0004", "Overhead Water Tank Repair & Pipeline Extension", "water-supply", "Pipeline extension and tank repair under Jal Jeevan Mission. [Sample Demo Data]", "School Tola", wards[2], 26.7720, 83.1780, 1200000, 1200000, 300000, "Jal Jeevan Mission", ProjectStatus.IN_PROGRESS, 40),
            ("PRJ-2026-0005", "Primary School Smart Class & Lab Upgradation", "schools", "Upgradation of classrooms with smart boards and computer desk. [Sample Demo Data]", "School Tola", wards[2], 26.7722, 83.1782, 950000, 950000, 950000, "Sarva Shiksha Abhiyan", ProjectStatus.COMPLETED, 100),
            ("PRJ-2026-0006", "Tenuhari Sub-Centre Health Clinic Addition", "health-facilities", "Adding patient observation ward and doctor room at health sub-centre. [Sample Demo Data]", "Purab Tola", wards[5], 26.7705, 83.1765, 2500000, 2500000, 1000000, "National Health Mission", ProjectStatus.IN_PROGRESS, 45),
            ("PRJ-2026-0007", "Gram Panchayat Open Gym & Children Park", "parks", "Landscaping, swings, walking track, and open gym equipment. [Sample Demo Data]", "Shukla Mohalla", wards[1], 26.7730, 83.1790, 500000, 500000, 500000, "Panchayat Own Resources", ProjectStatus.COMPLETED, 100),
            ("PRJ-2026-0008", "Solid Waste Segregation & Composting Unit", "waste-management", "Building organic waste composting unit and plastic collection shed. [Sample Demo Data]", "Sahjanwa Marg", wards[3], 26.7740, 83.1800, 750000, 750000, 200000, "Swachh Bharat Abhiyan", ProjectStatus.IN_PROGRESS, 30),
            ("PRJ-2026-0009", "Panchayat Power Grid Transformer Upgradation", "electricity", "Replacing 100kVA transformer with 250kVA unit to ensure voltage stability. [Sample Demo Data]", "Panchayat Bhawan Tola", wards[4], 26.7745, 83.1805, 400000, 400000, 400000, "UP Power Corp", ProjectStatus.COMPLETED, 100),
            ("PRJ-2026-0010", "Gram Panchayat Bhawan Community Hall Renovation", "other", "Repainting, floor tiling, and soundproofing of Community Hall. [Sample Demo Data]", "Panchayat Bhawan Tola", wards[4], 26.7715, 83.1775, 650000, 650000, 150000, "Panchayat Revenue", ProjectStatus.IN_PROGRESS, 25),
            ("PRJ-2026-0011", "School Tola Piped Water Line Extension", "water-supply", "Laying underground HDPE water pipes to connect 150 households. [Sample Demo Data]", "School Tola", wards[2], 26.7723, 83.1783, 1100000, 1100000, 0, "Jal Jeevan Mission", ProjectStatus.APPROVED, 0),
            ("PRJ-2026-0012", "Interlocking Paver Block Alleyways", "roads", "Laying heavy-duty paver blocks in residential lanes of Shukla Mohalla. [Sample Demo Data]", "Shukla Mohalla", wards[1], 26.7729, 83.1789, 450000, 450000, 450000, "State Local Fund", ProjectStatus.COMPLETED, 100),
            ("PRJ-2026-0013", "Gram Panchayat Digital Reading Room & Library", "schools", "Quiet public reading room equipped with 8 computers and Wi-Fi. [Sample Demo Data]", "Tenuhari Khas", wards[0], 26.7712, 83.1772, 800000, 800000, 0, "Panchayat Innovation Fund", ProjectStatus.PLANNED, 0),
            ("PRJ-2026-0014", "Deep Borewell Handpump Installation (8 Units)", "water-supply", "Drilling deep borewell handpumps in remote residential clusters. [Sample Demo Data]", "All Wards", wards[0], 26.7716, 83.1776, 350000, 350000, 350000, "MP LAD Scheme", ProjectStatus.COMPLETED, 100),
            ("PRJ-2026-0015", "Market Intersection CCTV Security Network", "other", "Installation of 12 HD CCTV cameras with central monitoring at Panchayat Bhawan. [Sample Demo Data]", "Panchayat Bhawan Tola", wards[4], 26.7718, 83.1778, 300000, 300000, 300000, "Safety Fund", ProjectStatus.COMPLETED, 100),
            ("PRJ-2026-0016", "Ward 4 Storm Water Discharge Outlet Cleanout", "drainage", "Cleaning and widening main discharge culvert near Sahjanwa road. [Sample Demo Data]", "Sahjanwa Marg", wards[3], 26.7738, 83.1798, 280000, 280000, 140000, "Disaster Management Fund", ProjectStatus.IN_PROGRESS, 50),
            ("PRJ-2026-0017", "Public Sanitation Complex Construction", "other", "Modern 6-seat public sanitation complex near main road stop. [Sample Demo Data]", "Sahjanwa Marg", wards[3], 26.7742, 83.1802, 550000, 550000, 550000, "Swachh Bharat Abhiyan", ProjectStatus.COMPLETED, 100),
            ("PRJ-2026-0018", "Veterinary Care Mobile Unit Store & Shelter", "health-facilities", "Building shelter and store for visiting livestock medical team. [Sample Demo Data]", "Purab Tola", wards[5], 26.7708, 83.1768, 320000, 320000, 0, "Animal Husbandry Fund", ProjectStatus.PLANNED, 0),
            ("PRJ-2026-0019", "Solar High-Mast Floodlight at Main Square", "street-lights", "Installation of 14-meter high mast floodlight at central square. [Sample Demo Data]", "Panchayat Bhawan Tola", wards[4], 26.7719, 83.1779, 220000, 220000, 220000, "District Innovation Fund", ProjectStatus.COMPLETED, 100),
            ("PRJ-2026-0020", "Farmer Produce Harvest Storage Warehouse", "other", "Constructing storage shed for local vegetable and grain harvest. [Sample Demo Data]", "Panchayat Bhawan Tola", wards[4], 26.7744, 83.1804, 1800000, 1800000, 450000, "NABARD Grant", ProjectStatus.IN_PROGRESS, 25),
        ]

        created_projects = []
        for pid, name, cslug, desc, loc, ward, lat, lng, est, app_b, spent, fsrc, status, prog in projects_data:
            proj, _ = DevelopmentProject.objects.update_or_create(
                project_id=pid,
                defaults={
                    "name": name,
                    "category": cat_map[cslug],
                    "description": desc,
                    "location": loc,
                    "village": village,
                    "ward": ward,
                    "latitude": lat,
                    "longitude": lng,
                    "estimated_cost": est,
                    "approved_budget": app_b,
                    "amount_spent": spent,
                    "funding_source": fsrc,
                    "start_date": timezone.now().date() - timedelta(days=random.randint(30, 180)),
                    "expected_completion_date": timezone.now().date() + timedelta(days=random.randint(30, 120)),
                    "actual_completion_date": timezone.now().date() if status == ProjectStatus.COMPLETED else None,
                    "contractor": "Sahjanwa Rural Infra Contractors",
                    "status": status,
                    "progress_percentage": prog,
                    "created_by": panchayat_admin
                }
            )
            created_projects.append(proj)

            if spent > 0:
                ProjectExpense.objects.get_or_create(
                    project=proj,
                    title="Material Supply & Foundation Excavation",
                    defaults={
                        "amount": spent * 0.6,
                        "spent_date": timezone.now().date() - timedelta(days=20),
                        "invoice_number": f"INV-{random.randint(1000, 9999)}",
                        "description": "Cement, gravel, steel rods, and JCB equipment rental."
                    }
                )

            ProjectTimeline.objects.get_or_create(
                project=proj,
                title="Project Approved at Gram Sabha",
                defaults={
                    "event_date": timezone.now().date() - timedelta(days=60),
                    "status_reached": ProjectStatus.APPROVED,
                    "description": "Sanctioned during Gram Sabha meeting under Sarpanch MOHANLAL."
                }
            )

        # 5. Complaints
        complaint_cats = [
            ("Road Damage", "Damaged asphalt, potholes, and broken paving"),
            ("Drainage/Gutter", "Overflowing or clogged drains"),
            ("Water Supply", "Pipeline leaks, low pressure, or handpump breakdown"),
            ("Street Light", "Fused LED bulbs or broken poles"),
            ("Waste Management", "Garbage buildup or uncleaned bin"),
            ("Electricity", "Voltage fluctuation or loose wire"),
            ("Public Toilet", "Sanitation or water availability issues"),
            ("Other", "General civic issues"),
        ]
        ccat_objects = []
        for cname, cdesc in complaint_cats:
            ccat, _ = ComplaintCategory.objects.get_or_create(name=cname, defaults={"description": cdesc})
            ccat_objects.append(ccat)

        complaints_data = [
            ("CMP-2026-0001", villagers[0], ccat_objects[0], "Pothole near Primary School Entrance", "Near Primary School, School Tola", wards[2], ComplaintPriority.HIGH, ComplaintStatus.IN_PROGRESS),
            ("CMP-2026-0002", villagers[1], ccat_objects[2], "Handpump Handle Broken in Shukla Mohalla", "Shukla Mohalla Lane 2", wards[1], ComplaintPriority.URGENT, ComplaintStatus.RESOLVED),
            ("CMP-2026-0003", villagers[2], ccat_objects[3], "Streetlight Fused on Sahjanwa Road", "Pole #14, Sahjanwa Marg", wards[3], ComplaintPriority.MEDIUM, ComplaintStatus.RESOLVED),
            ("CMP-2026-0004", villagers[3], ccat_objects[1], "Clogged Drain Waterlogging in Ward 4", "Sahjanwa Marg Lane 3", wards[3], ComplaintPriority.HIGH, ComplaintStatus.ACKNOWLEDGED),
            ("CMP-2026-0005", villagers[0], ccat_objects[4], "Uncollected Waste at Market Corner", "Panchayat Bhawan Square", wards[4], ComplaintPriority.MEDIUM, ComplaintStatus.SUBMITTED),
            ("CMP-2026-0006", villagers[1], ccat_objects[5], "Low Voltage Issue in Shukla Mohalla", "Shukla Mohalla", wards[1], ComplaintPriority.HIGH, ComplaintStatus.ASSIGNED),
            ("CMP-2026-0007", villagers[2], ccat_objects[2], "Water Pipeline Leakage near Water Tank", "School Tola", wards[2], ComplaintPriority.URGENT, ComplaintStatus.IN_PROGRESS),
            ("CMP-2026-0008", villagers[3], ccat_objects[6], "Public Toilet Sanitation Maintenance Needed", "Main Bus Stop Complex", wards[3], ComplaintPriority.MEDIUM, ComplaintStatus.RESOLVED),
            ("CMP-2026-0009", villagers[0], ccat_objects[0], "Loose Concrete Paver Blocks", "Tenuhari Khas Lane 1", wards[0], ComplaintPriority.LOW, ComplaintStatus.SUBMITTED),
            ("CMP-2026-0010", villagers[1], ccat_objects[3], "Solar Lamp Battery Replacement", "Shukla Mohalla Park", wards[1], ComplaintPriority.LOW, ComplaintStatus.SUBMITTED),
            ("CMP-2026-0011", villagers[2], ccat_objects[1], "Side Gutter Overflow after Rain", "School Tola Main St", wards[2], ComplaintPriority.HIGH, ComplaintStatus.IN_PROGRESS),
            ("CMP-2026-0012", villagers[3], ccat_objects[4], "Dustbin Lid Repair", "Sahjanwa Marg Stop", wards[3], ComplaintPriority.LOW, ComplaintStatus.CLOSED),
            ("CMP-2026-0013", villagers[0], ccat_objects[5], "Tree Branch Touching Wire", "Panchayat Bhawan Road", wards[4], ComplaintPriority.HIGH, ComplaintStatus.RESOLVED),
            ("CMP-2026-0014", villagers[1], ccat_objects[0], "Culvert Masonry Repair Required", "Purab Tola Bypass", wards[5], ComplaintPriority.MEDIUM, ComplaintStatus.ACKNOWLEDGED),
            ("CMP-2026-0015", villagers[2], ccat_objects[2], "Handpump Water Turbidity", "Tenuhari Khas Block B", wards[0], ComplaintPriority.URGENT, ComplaintStatus.IN_PROGRESS),
        ]

        for ticket, user, ccat, title, loc, ward, priority, status in complaints_data:
            cmp_obj, _ = Complaint.objects.update_or_create(
                ticket_number=ticket,
                defaults={
                    "user": user,
                    "category": ccat,
                    "title": title,
                    "description": f"Civic report: {title}. Requires prompt Gram Panchayat maintenance action.",
                    "location": loc,
                    "village": village,
                    "ward": ward,
                    "priority": priority,
                    "status": status,
                    "internal_notes": "Assigned to Panchayat Secretary / Maintenance team.",
                    "resolution_comment": "Inspected and resolved by Ward Maintenance Supervisor." if status in [ComplaintStatus.RESOLVED, ComplaintStatus.CLOSED] else ""
                }
            )

            ComplaintUpdate.objects.get_or_create(
                complaint=cmp_obj,
                status=status,
                defaults={
                    "note": f"Complaint status updated to {cmp_obj.get_status_display()}.",
                    "updated_by": panchayat_admin,
                    "is_public": True
                }
            )

        # 6. 10 Government Schemes
        schemes_data = [
            ("Pradhan Mantri Awas Yojana (PMAY-G)", "pmay-g", SchemeCategory.HOUSING, "Ministry of Rural Development", "Financial assistance of ₹1.20 Lakh for building pucca houses for homeless and kutcha house dwellers in rural Panchayats.", "Income less than ₹3 Lakh/year, kutcha house owner in Tenuhari.", "₹1,20,000 direct bank transfer in 3 installments.", "Aadhaar Card, Bank Passbook, Land ownership proof (Khatauni)", "Apply online through Gram Panchayat CSC operator.", "https://pmayg.nic.in"),
            ("PM-KISAN Samman Nidhi", "pm-kisan", SchemeCategory.AGRICULTURE, "Department of Agriculture", "Direct income support of ₹6,000 per year in three equal installments to small & marginal farmers.", "Land-holding farmer families in Sahjanwa Tehsil.", "₹6,000 per year direct benefit transfer.", "Land Records (Khatauni), Aadhaar Card, Bank Account", "Self-registration on PM-KISAN portal or via Panchayat CSC.", "https://pmkisan.gov.in"),
            ("MGNREGA Employment Guarantee", "mgnrega", SchemeCategory.EMPLOYMENT, "Ministry of Rural Development", "Provides 100 days guaranteed wage employment per year for unskilled manual work in Panchayat development.", "Adult members of rural households willing to do manual work.", "Guaranteed daily wages credited directly to bank account.", "Job Card application, Aadhaar Card, Passport photo", "Submit application to Gram Panchayat Secretary for Job Card.", "https://nrega.nic.in"),
            ("Old Age Pension Scheme (Social Welfare)", "old-age-pension", SchemeCategory.PENSION, "Social Welfare Department UP", "Monthly pension support of ₹1,000 to senior citizens living below poverty line.", "Age 60 years and above, BPL card holder resident of UP.", "₹1,000 per month pension credit.", "Age Proof, Income Certificate, Bank Passbook, Aadhaar", "Fill application form at Gram Panchayat office.", "https://sspy-up.gov.in"),
            ("Ayushman Bharat PM-JAY", "ayushman-bharat", SchemeCategory.HEALTH, "National Health Authority", "Health cover of ₹5 Lakh per family per year for secondary and tertiary hospitalization.", "SECC database listed families and BPL card holders.", "Free cashless medical treatment up to ₹5 Lakh at empanelled hospitals.", "Ayushman Card or Ration Card + Aadhaar", "Generate card at Community Health Centre or Panchayat CSC.", "https://pmjay.gov.in"),
            ("Kanya Sumangala Yojana", "kanya-sumangala", SchemeCategory.WOMEN_CHILD, "Women & Child Development UP", "Financial assistance of ₹15,000 in six phases for girl child health and education.", "Resident of UP, family income less than ₹3 Lakh, max 2 girls.", "₹15,000 total monetary assistance.", "Birth Certificate, Family Photo, Bank Account, Aadhaar", "Apply online on Kanya Sumangala portal.", "https://mksy.up.gov.in"),
            ("Subsidized Solar Water Pump Scheme", "solar-pump", SchemeCategory.AGRICULTURE, "UP Renewable Energy Dept", "Up to 75% subsidy on solar water pumps for agricultural irrigation.", "Farmers owning agricultural land in Sahjanwa area with borewell connection.", "75% subsidy on 3HP to 7.5HP solar pumps.", "Land Khatauni, Electricity Bill, Aadhaar, Bank Details", "Apply online on UP Agriculture portal.", "https://upagriculture.com"),
            ("Mukhyamantri Yuva Swarojgar Yojana", "yuva-swarojgar", SchemeCategory.EMPLOYMENT, "Industry Department UP", "Collateral-free loans up to ₹25 Lakh for young entrepreneurs setting up rural enterprises.", "Age 18-40 years, Minimum Class 10 pass.", "Loan up to ₹25 Lakh with 25% margin money subsidy.", "Project Report, Marksheet, Aadhaar, Bank Details", "Submit business proposal online.", "https://diupmsme.upsdc.gov.in"),
            ("Divyangjan Pension Scheme", "divyang-pension", SchemeCategory.PENSION, "Disabled Welfare Dept UP", "Financial aid of ₹1,000 per month for persons with disabilities.", "Minimum 40% disability certificate holder.", "₹1,000 monthly financial aid.", "Disability Certificate, Aadhaar, Bank Passbook", "Apply at Panchayat Office or District Social Welfare.", "https://sspy-up.gov.in"),
            ("Chief Minister Farmer Accident Kalyan Scheme", "farmer-accident", SchemeCategory.FINANCIAL, "Revenue Department UP", "Financial aid of ₹5 Lakh to family in case of accidental death/disability of farmer.", "Farmers and registered agricultural laborers aged 18-70 in Gorakhpur district.", "₹5,00,000 compensation to legal heir.", "Death/Disability Certificate, FIR copy, Land record", "Submit claim to Tehsil Sahjanwa / Gram Panchayat within 45 days.", "https://bor.up.nic.in"),
        ]

        for sname, sslug, scat, sdept, sdesc, selig, sben, srdoc, sapp, slink in schemes_data:
            GovernmentScheme.objects.update_or_create(
                slug=sslug,
                defaults={
                    "name": sname,
                    "category": scat,
                    "department": sdept,
                    "description": sdesc,
                    "eligibility": selig,
                    "benefits": sben,
                    "required_documents": srdoc,
                    "application_process": sapp,
                    "deadline": timezone.now().date() + timedelta(days=120),
                    "official_link": slink,
                    "is_active": True
                }
            )

        # 7. 10 Panchayat Services
        services_data = [
            ("Residence Certificate Application", "residence-certificate", "Certificates & Documents", "Official certificate proving continuous residence in Tenuhari (Shukla) village.", "Resident of Tenuhari (Shukla) for at least 3 years.", "Aadhaar Card\nElectricity/Ration Bill\nSelf Declaration Form", 7, 50.00),
            ("Income Certificate Verification", "income-certificate", "Certificates & Documents", "Verified certificate detailing family annual income for welfare schemes.", "Head of household residing in Gram Panchayat.", "Aadhaar Card\nSalary Slip/Income Declaration\nRation Card", 5, 50.00),
            ("Birth Registration Request", "birth-registration", "Vital Events", "Official birth registration and certificate issuance for newborn child.", "Birth occurred within Tenuhari (Shukla) Panchayat jurisdiction.", "Hospital Discharge Slip\nParents' Aadhaar Cards\nMarriage Proof", 10, 0.00),
            ("Death Registration Request", "death-registration", "Vital Events", "Official death certificate registration and issuance.", "Death occurred within Tenuhari Panchayat area.", "Hospital Doctor Certificate / Cremation Slip\nDeceased Aadhaar\nApplicant Photo", 10, 0.00),
            ("Water Connection Pipeline Request", "water-connection", "Public Utilities", "New household drinking water tap pipeline connection request.", "Owner or registered tenant of house in Tenuhari (Shukla).", "Property Tax Receipt\nAadhaar Card\nHouse Layout Sketch", 14, 250.00),
            ("Panchayat NOC for Construction", "panchayat-noc", "NOC & Approvals", "No Objection Certificate for residential building construction.", "Land owner in Tenuhari (Shukla) village.", "Land Ownership Document (Khatauni)\nBuilding Layout Map\nAadhaar", 15, 500.00),
            ("Old Age Pension Recommendation", "pension-recommendation", "Social Security", "Gram Sabha recommendation letter for state senior citizen pension.", "Age 60+ BPL resident.", "Age Proof Certificate\nAadhaar Card\nBank Passbook", 7, 0.00),
            ("Character & Conduct Certificate", "character-certificate", "Certificates & Documents", "Character verification certificate issued by Sarpanch MOHANLAL / Secretary.", "Resident of Tenuhari (Shukla) with no criminal record.", "Aadhaar Card\nPolice Verification (if any)\n2 Passport Photos", 3, 20.00),
            ("Caste & Community Verification", "caste-verification", "Certificates & Documents", "Panchayat verification of community status for government quotas.", "Resident belonging to SC/ST/OBC category.", "Ancestral Land Records\nFather's Caste Cert (if available)\nAadhaar", 7, 30.00),
            ("Streetlight Repair Request", "streetlight-repair-request", "Public Utilities", "Special service request for installing or fixing street lighting.", "Resident of Ward 1 to 6.", "Aadhaar Card\nLocation Landmark", 3, 0.00),
        ]

        created_services = []
        for sname, sslug, scat, sdesc, selig, srdoc, spdays, sfee in services_data:
            service, _ = PanchayatService.objects.update_or_create(
                slug=sslug,
                defaults={
                    "name": sname,
                    "category": scat,
                    "description": sdesc,
                    "eligibility": selig,
                    "required_documents": srdoc,
                    "processing_days": spdays,
                    "fee": sfee,
                    "is_active": True
                }
            )
            created_services.append(service)

            for doc_line in srdoc.split('\n'):
                if doc_line.strip():
                    ServiceRequirement.objects.get_or_create(
                        service=service,
                        document_name=doc_line.strip(),
                        defaults={"is_mandatory": True}
                    )

        # 8. Service Applications
        applications_data = [
            ("APP-2026-0001", villagers[0], created_services[0], "Ramesh Kumar", "9988776655", "House #14, Tenuhari Khas, Ward 1", ApplicationStatus.APPROVED, "Verified by Ward Member."),
            ("APP-2026-0002", villagers[1], created_services[1], "Sita Devi", "9988776654", "House #45, Shukla Mohalla, Ward 2", ApplicationStatus.UNDER_VERIFICATION, "Field verification scheduled."),
            ("APP-2026-0003", villagers[2], created_services[2], "Amit Sharma", "9988776653", "House #89, School Tola, Ward 3", ApplicationStatus.APPROVED, "Birth certificate issued."),
            ("APP-2026-0004", villagers[3], created_services[4], "Priya Singh", "9988776652", "House #102, Sahjanwa Marg, Ward 4", ApplicationStatus.SUBMITTED, "Awaiting plumber inspection."),
            ("APP-2026-0005", villagers[0], created_services[5], "Ramesh Kumar", "9988776655", "House #14, Tenuhari Khas, Ward 1", ApplicationStatus.REJECTED, "Land title document incomplete."),
            ("APP-2026-0006", villagers[1], created_services[6], "Sita Devi", "9988776654", "House #45, Shukla Mohalla, Ward 2", ApplicationStatus.APPROVED, "Gram Sabha recommendation granted."),
            ("APP-2026-0007", villagers[2], created_services[7], "Amit Sharma", "9988776653", "House #89, School Tola, Ward 3", ApplicationStatus.SUBMITTED, "Submitted online."),
            ("APP-2026-0008", villagers[3], created_services[8], "Priya Singh", "9988776652", "House #102, Sahjanwa Marg, Ward 4", ApplicationStatus.UNDER_VERIFICATION, "Document check in progress."),
            ("APP-2026-0009", villagers[0], created_services[1], "Ramesh Kumar", "9988776655", "House #14, Tenuhari Khas, Ward 1", ApplicationStatus.APPROVED, "Income verified at ₹1,20,000."),
            ("APP-2026-0010", villagers[1], created_services[3], "Sita Devi", "9988776654", "House #45, Shukla Mohalla, Ward 2", ApplicationStatus.APPROVED, "Death certificate registered."),
        ]

        for app_num, applicant, serv, app_name, app_phone, app_addr, status, remarks in applications_data:
            ServiceApplication.objects.update_or_create(
                application_number=app_num,
                defaults={
                    "applicant": applicant,
                    "service": serv,
                    "village": village,
                    "ward": applicant.ward,
                    "applicant_name": app_name,
                    "applicant_phone": app_phone,
                    "applicant_address": app_addr,
                    "status": status,
                    "remarks": remarks,
                    "rejection_reason": "Missing clear Khatauni land title proof." if status == ApplicationStatus.REJECTED else "",
                    "processed_by": panchayat_admin if status != ApplicationStatus.SUBMITTED else None,
                    "processed_at": timezone.now() if status != ApplicationStatus.SUBMITTED else None
                }
            )

        # 9. 10 Notices
        notices_data = [
            ("Special Gram Sabha Meeting Notice - Annual Budget Approval", "gram-sabha-annual-budget-2026", NoticeCategory.GRAM_SABHA, "All villagers of Tenuhari (Shukla) are invited to attend Gram Sabha meeting presided by Sarpanch MOHANLAL on 10th of next month at Panchayat Bhawan.", True),
            ("Drinking Water Supply Maintenance Notice", "water-supply-schedule-change", NoticeCategory.WATER_SUPPLY, "Due to pipeline maintenance work under Jal Jeevan Mission, water supply will be available from 6:00 AM to 8:30 AM tomorrow.", True),
            ("Free Health & Eye Checkup Camp at Tenuhari Sub-Centre", "health-camp-tenuhari", NoticeCategory.HEALTH_CAMP, "A free health checkup camp organized by Sahjanwa CHC will be held at Tenuhari Health Sub-centre on Sunday.", False),
            ("Road Work Traffic Advisory - Sahjanwa Marg", "road-paving-alert-sahjanwa-road", NoticeCategory.ROAD_WORK, "Sahjanwa Marg lane near Panchayat Bhawan will remain closed for heavy traffic for 3 days for paver block curing.", False),
            ("Enrollment Open for PM-KISAN 16th Installment", "pm-kisan-16th-installment-open", NoticeCategory.SCHEME, "Farmers whose e-KYC is pending can visit Tenuhari Gram Panchayat CSC kiosk before the 25th of this month.", False),
            ("Swachh Tenuhari Plantation & Cleanliness Campaign", "cleanliness-plantation-drive", NoticeCategory.GENERAL, "Join Sarpanch MOHANLAL and village youth this Saturday for a sapling plantation drive around the Panchayat pond.", False),
            ("Heavy Rain & Thunderstorm Advisory", "heavy-rain-alert-precautions", NoticeCategory.EMERGENCY, "Meteorological department warns of monsoon thunderstorm across Gorakhpur district. Keep livestock in safe shelter.", True),
            ("Child & Maternal Routine Immunization Drive", "vaccination-drive-children", NoticeCategory.HEALTH_CAMP, "Anganwadi centers across Wards 1 to 6 will conduct routine immunization tomorrow from 9:00 AM.", False),
            ("Applications Invited for Solar Lighting Maintenance Operator", "solar-light-maintenance-crew", NoticeCategory.GENERAL, "Local ITI pass candidates can submit applications at Panchayat office for solar lighting maintenance contract.", False),
            ("Primary School Admissions Open for Session 2026-27", "school-admissions-open-2026", NoticeCategory.EDUCATION, "Admissions open for Class 1 to 5 at Tenuhari Primary School. Free textbooks and uniforms provided.", False),
        ]

        for ntitle, nslug, ncat, ndesc, npinned in notices_data:
            Notice.objects.update_or_create(
                slug=nslug,
                defaults={
                    "title": ntitle,
                    "category": ncat,
                    "description": ndesc,
                    "published_by": panchayat_admin,
                    "is_pinned": npinned,
                    "is_published": True,
                    "expiry_date": timezone.now().date() + timedelta(days=60)
                }
            )

        # 10. 20 Infrastructure Map Markers (Leaflet OSM Centered at Sahjanwa/Tenuhari ~26.7725, 83.1783)
        infra_data = [
            ("Tenuhari Gram Panchayat Bhawan", InfraCategory.PANCHAYAT_BHAWAN, "Central Administrative Office & CSC Kiosk [Sample Demo Data]", 26.7725, 83.1783, wards[4], InfraStatus.OPERATIONAL),
            ("Tenuhari Primary School", InfraCategory.SCHOOL, "Government Primary School with Smart Classroom [Sample Demo Data]", 26.7722, 83.1782, wards[2], InfraStatus.OPERATIONAL),
            ("Tenuhari Health Sub-Centre", InfraCategory.HEALTH_CENTRE, "Primary Care Clinic & Immunization Hub [Sample Demo Data]", 26.7705, 83.1765, wards[5], InfraStatus.OPERATIONAL),
            ("Jal Jeevan Overhead Water Tank", InfraCategory.WATER_TANK, "Community Drinking Water Overhead Tank [Sample Demo Data]", 26.7720, 83.1780, wards[2], InfraStatus.OPERATIONAL),
            ("Sahjanwa Marg CC Road Project", InfraCategory.ROAD_PROJECT, "2.2 km CC Road Paving with Covered Drain [Sample Demo Data]", 26.7735, 83.1795, wards[3], InfraStatus.PROPOSED),
            ("Panchayat Square Solar High-Mast Light", InfraCategory.STREET_LIGHT, "14m Quad LED High Mast Light Unit [Sample Demo Data]", 26.7719, 83.1779, wards[4], InfraStatus.OPERATIONAL),
            ("Shukla Mohalla Park & Open Gym", InfraCategory.PARK, "Green Park with Open Gym Equipment [Sample Demo Data]", 26.7730, 83.1790, wards[1], InfraStatus.OPERATIONAL),
            ("Main Bus Stop Sanitation Complex", InfraCategory.PUBLIC_TOILET, "Modern Public Sanitation Complex [Sample Demo Data]", 26.7742, 83.1802, wards[3], InfraStatus.OPERATIONAL),
            ("Waste Composting & Segregation Shed", InfraCategory.WASTE_COLLECTION, "Organic Waste Composting Facility [Sample Demo Data]", 26.7740, 83.1800, wards[3], InfraStatus.OPERATIONAL),
            ("Ward 1 Deep Borewell Handpump #1", InfraCategory.HAND_PUMP, "Deep Borewell Handpump - Clean Water [Sample Demo Data]", 26.7710, 83.1770, wards[0], InfraStatus.OPERATIONAL),
            ("Ward 2 Deep Borewell Handpump #2", InfraCategory.HAND_PUMP, "Public Drinking Handpump [Sample Demo Data]", 26.7729, 83.1789, wards[1], InfraStatus.OPERATIONAL),
            ("Ward 3 School Tola Handpump #3", InfraCategory.HAND_PUMP, "Public Drinking Water Handpump [Sample Demo Data]", 26.7723, 83.1783, wards[2], InfraStatus.OPERATIONAL),
            ("Power Grid Sub-station 250kVA", InfraCategory.PANCHAYAT_BHAWAN, "Grid Power Transformer Station [Sample Demo Data]", 26.7745, 83.1805, wards[4], InfraStatus.OPERATIONAL),
            ("Tenuhari Khas Covered Storm Drain", InfraCategory.ROAD_PROJECT, "Covered Storm Water Drain [Sample Demo Data]", 26.7712, 83.1772, wards[0], InfraStatus.OPERATIONAL),
            ("Sahjanwa Marg Solar Street Light Array", InfraCategory.STREET_LIGHT, "12 Solar LED Street Lamp Network [Sample Demo Data]", 26.7738, 83.1798, wards[3], InfraStatus.OPERATIONAL),
            ("Livestock Care Mobile Support Shelter", InfraCategory.HEALTH_CENTRE, "Veterinary Doctor Visit Shelter [Sample Demo Data]", 26.7708, 83.1768, wards[5], InfraStatus.OPERATIONAL),
            ("Sahjanwa Stop Waste Collection Point", InfraCategory.WASTE_COLLECTION, "Segregated Waste Dump Bins [Sample Demo Data]", 26.7741, 83.1801, wards[3], InfraStatus.OPERATIONAL),
            ("Panchayat Community Hall", InfraCategory.PANCHAYAT_BHAWAN, "Multi-purpose Hall for Gram Sabha & Events [Sample Demo Data]", 26.7715, 83.1775, wards[4], InfraStatus.OPERATIONAL),
            ("Purab Tola Handpump #4", InfraCategory.HAND_PUMP, "Public Deep Well Handpump [Sample Demo Data]", 26.7706, 83.1766, wards[5], InfraStatus.OPERATIONAL),
            ("Tenuhari Digital Library Kiosk", InfraCategory.SCHOOL, "E-Learning & Reading Room [Sample Demo Data]", 26.7726, 83.1786, wards[2], InfraStatus.PROPOSED),
        ]

        for iname, icat, idesc, ilat, ilng, iward, istat in infra_data:
            InfrastructureItem.objects.update_or_create(
                name=iname,
                defaults={
                    "category": icat,
                    "description": idesc,
                    "village": village,
                    "ward": iward,
                    "latitude": ilat,
                    "longitude": ilng,
                    "status": istat,
                    "created_by": panchayat_admin
                }
            )

        # 11. Gallery Items
        gallery_data = [
            ("Gram Sabha Meeting under Sarpanch MOHANLAL", GalleryCategory.GRAM_SABHA, "Villagers discussing development proposals at Gram Panchayat Bhawan."),
            ("Tree Plantation Drive at Tenuhari Primary School", GalleryCategory.PLANTATION, "Sapling plantation drive organized by Gram Panchayat."),
            ("Swachh Tenuhari Cleanliness Campaign", GalleryCategory.CLEANLINESS, "Volunteers cleaning main market road and installing dustbins."),
            ("Inauguration of Solar LED Lighting Network", GalleryCategory.DEVELOPMENT, "Sarpanch MOHANLAL inaugurating solar streetlights network."),
            ("Annual Rural Sports Event 2026", GalleryCategory.SPORTS, "Kabbadi and volleyball tournament final match at Tenuhari playground."),
            ("Digital Literacy Workshop for Women", GalleryCategory.EDUCATION, "Training villagers on online citizen services and smartphone usage."),
        ]

        for gtitle, gcat, gcap in gallery_data:
            GalleryItem.objects.update_or_create(
                title=gtitle,
                defaults={
                    "category": gcat,
                    "caption": gcap,
                    "event_date": timezone.now().date() - timedelta(days=random.randint(10, 90)),
                    "is_archived": False
                }
            )

        # 12. Project Feedback
        completed_projs = DevelopmentProject.objects.filter(status=ProjectStatus.COMPLETED)
        if completed_projs.exists():
            fb_proj = completed_projs.first()
            ProjectFeedback.objects.get_or_create(
                project=fb_proj,
                user=villagers[0],
                defaults={
                    "rating": 5,
                    "comment": "Excellent work! The new paver block road has made monsoon commuting hassle-free."
                }
            )

        # 13. Audit Log
        AuditLog.objects.create(
            actor=panchayat_admin,
            action="SEED_DATA_EXECUTION",
            model_name="System",
            object_id="1",
            description="GramSetu V2 localized seed data successfully updated for Tenuhari (Shukla), Sahjanwa, Gorakhpur.",
            ip_address="127.0.0.1"
        )

        self.stdout.write(self.style.SUCCESS("\n=================================================="))
        self.stdout.write(self.style.SUCCESS("[OK] GRAMSETU V2 TENUHARI SEED DATA SUCCESSFUL!"))
        self.stdout.write(self.style.SUCCESS("=================================================="))
        self.stdout.write(f"  Village: Tenuhari (Shukla), Sahjanwa, Gorakhpur, UP - 273209")
        self.stdout.write(f"  Sarpanch: MOHANLAL")
        self.stdout.write(f"  Projects Created: {DevelopmentProject.objects.count()}")
        self.stdout.write(f"  Complaints Created: {Complaint.objects.count()}")
        self.stdout.write(f"  Schemes Created: {GovernmentScheme.objects.count()}")
        self.stdout.write(f"  Notices Created: {Notice.objects.count()}")
        self.stdout.write(f"  Infrastructure Markers: {InfrastructureItem.objects.count()}")
        self.stdout.write(f"  Village Conditions: {VillageCondition.objects.count()}")
        self.stdout.write(f"  Related Panchayats: {RelatedPanchayat.objects.count()}")
        self.stdout.write(self.style.SUCCESS("\nDemo Credentials:"))
        self.stdout.write(self.style.WARNING("  Super Admin: username='admin' | password='admin12345'"))
        self.stdout.write(self.style.WARNING("  Sarpanch (Panchayat Admin): username='sarpanch' | password='admin12345'"))
        self.stdout.write(self.style.WARNING("  Villager User: username='ramesh' | password='pass12345'"))
        self.stdout.write(self.style.SUCCESS("==================================================\n"))
