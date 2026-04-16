import os
import django
from django.core.files import File
import urllib.request
from tempfile import NamedTemporaryFile

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
django.setup()

from shop.models import Category, Product, ProductImage

import ssl

def download_image(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    response = urllib.request.urlopen(url, context=ctx)
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(response.read())
    img_temp.flush()
    return img_temp

def seed_db():
    print("Clearing old data...")
    Product.objects.all().delete()
    Category.objects.all().delete()

    print("Creating Categories...")
    cat_gold = Category.objects.create(name="Bridal Gold", slug="bridal-gold")
    cat_diamond = Category.objects.create(name="Diamond Collection", slug="diamond-collection")
    cat_silver = Category.objects.create(name="Silver Antiques", slug="silver-antiques")

    print("Downloading Images and Creating Products...")

    # Product 1 with Multiple Images for Slider
    p1 = Product.objects.create(title="Royal Rani Haar", description="24K pure gold bridal necklace set.", price="250000.00", category=cat_gold, is_featured=True)
    img1_1 = download_image("https://picsum.photos/seed/necklace1/600/800")
    ProductImage.objects.create(product=p1, image=File(img1_1, name="gold_necklace_1.jpg"), is_primary=True)
    img1_2 = download_image("https://picsum.photos/seed/necklace2/600/800")
    ProductImage.objects.create(product=p1, image=File(img1_2, name="gold_necklace_2.jpg"), is_primary=False)
    img1_3 = download_image("https://picsum.photos/seed/necklace3/600/800")
    ProductImage.objects.create(product=p1, image=File(img1_3, name="gold_necklace_3.jpg"), is_primary=False)

    # Product 2
    p2 = Product.objects.create(title="Solitaire Diamond Ring", description="VVS1 clarity 1-carat diamond ring in platinum.", price="185000.00", category=cat_diamond, is_featured=True)
    img2 = download_image("https://picsum.photos/seed/ring1/600/800")
    ProductImage.objects.create(product=p2, image=File(img2, name="diamond_ring.jpg"), is_primary=True)

    # Product 3
    p3 = Product.objects.create(title="Kundan Choker", description="Traditional Kundan artistry for weddings.", price="120000.00", category=cat_gold, is_featured=True)
    img3 = download_image("https://picsum.photos/seed/choker1/600/800")
    ProductImage.objects.create(product=p3, image=File(img3, name="kundan_choker.jpg"), is_primary=True)

    # Product 4
    p4 = Product.objects.create(title="Antique Silver Payal", description="Heavy silver anklets with detailed carving.", price="15000.00", category=cat_silver, is_featured=False)
    img4 = download_image("https://picsum.photos/seed/payal1/600/800")
    ProductImage.objects.create(product=p4, image=File(img4, name="silver_payal.jpg"), is_primary=True)

    # Product 5
    p5 = Product.objects.create(title="Diamond Stud Earrings", description="Elegant daily-wear diamond studs.", price="45000.00", category=cat_diamond, is_featured=True)
    img5 = download_image("https://picsum.photos/seed/stud1/600/800")
    ProductImage.objects.create(product=p5, image=File(img5, name="diamond_studs.jpg"), is_primary=True)

    # Product 6
    p6 = Product.objects.create(title="Temple Gold Bangles", description="Set of two 22K gold bangles.", price="85000.00", category=cat_gold, is_featured=False)
    img6 = download_image("https://picsum.photos/seed/bangle1/600/800") 
    ProductImage.objects.create(product=p6, image=File(img6, name="gold_bangles.jpg"), is_primary=True)

    print("Success! Database seeded with dummy products.")

if __name__ == '__main__':
    seed_db()
