from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Item, RSVP, Friend
from .serializers import ItemSerializer, RSVPSerializer, FriendSerializer
from rest_framework.response import Response


def send_email(destination, html):
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    sender_email = "matrimoniogiovannapietro@gmail.com"
    receiver_email = destination
    password = "minuuhoyrmnnjnze"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Matrimonio Giovanna & Pietro"
    message["From"] = sender_email
    message["To"] = receiver_email
    message.attach(MIMEText(html, "html"))
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )




def make_html(giftGiver, price):
    html_content = """
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ringraziamento</title>
        <style>
            body {{
                margin: 0;
                padding: 20px;
            }}

            h1 {{
                text-align: center;
                padding: 1rem;
            }}
            p {{
                text-align: center;
            }}
            .container {{
                padding: 4rem;
            }}

        </style>
    </head>
    <body class="cart-page">

        <div class="container" style="background-color: #FAF0CC !important">
        <h1>Grazie mille!</h1>
        <p>Grazie {0} per il tuo contributo!</p>
        <p>Puoi completare il regalo, effettuando il pagamento di <strong> {1} € </strong> tramite un bonifico bancario al seguente IBAN:</p>
        <p></p>
        <p style="font-size: 2rem">IT54K0503411901000000030670</p>
        </div>
    </body>
    </html>
    """.format(giftGiver, price)
    return html_content


def index(request):
    return render(request, 'wedding/index.html')

def rsvp(request):
    return render(request, 'wedding/rsvp.html')

def gift_list(request):
    return render(request, 'wedding/gift_list.html')



def cart(request):
    return render(request, 'wedding/cart-page.html')

def summary(request):
    return render(request, 'wedding/summary-page.html')

def thanks(request):
    return render(request, 'wedding/thanks.html')


def survey(request):
    return render(request, 'wedding/survey.html')


def dashboard(request):
    rsvps = RSVP.objects.all()
    friends = Friend.objects.all()
    context = {
        'rsvps': rsvps,
        'friends': friends
    }
    return render(request, 'wedding/dashboard.html', context)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class RSVPViewSet(viewsets.ModelViewSet):
    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer

class FriendViewSet(viewsets.ModelViewSet):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

    def create(self, request, *args, **kwargs):
        items = request.data.pop('string_ids', [])
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            for item in items:
                item_id, item_quantity = item.split('-')
                current = Item.objects.get(id=item_id)
                current.quantity -= int(item_quantity)
                current.save()      
            html = make_html(request.data.get('name', ''),request.data.get('item_price', ''))      
            send_email(request.data.get('email', ''), html)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
