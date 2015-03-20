from gm.models import Car, GasStation
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

class IndexView(generic.ListView):
    template_name = 'gm/index.html'
    context_object_name = 'car_list'

    def get_queryset(self):
        return Car.objects.raw('SELECT * FROM gm_car')

class TestView(generic.ListView):
	template_name = 'gm/test.html'
	def get_queryset(self):
		return Car.objects.all()

class AddCarView(generic.ListView):
	template_name = 'gm/addcar.html'
	def get_queryset(self):
		return Car.objects.raw('SELECT * FROM gm_car')

class EditCarView(generic.DetailView):
	model = Car
	template_name = 'gm/editcar.html'

def result(request, locationzip):
	cursor = connection.cursor()
	cursor.execute("SELECT address FROM tmpaddr")
	row = cursor.fetchone()
	sqllocation = row[0]
	tmploc = sqllocation.split(", ")
	strloc = tmploc[1]
	print strloc
	station = GasStation.objects.raw('SELECT * FROM gm_gasstation WHERE location LIKE %s', ("%" + strloc + "%",))
	#station = GasStation.objects.raw('SELECT * FROM gm_gasstation')

	cursor = connection.cursor()
	cursor.execute("SELECT address FROM tmpaddr")
	addre = cursor.fetchone()
	return render(request, 'gm/result.html', {'station_list': station, 'addr':addre[0], 'vmpg':locationzip})

def trip(request, locationzip):
    cursor = connection.cursor()
    cursor.execute("SELECT address FROM tmpaddr")
    row = cursor.fetchone()
    sqllocation = row[0]
    tmploc = sqllocation.split(", ")
    strloc = tmploc[1]
    cursor.execute("SELECT address FROM tmpdest")
    row2 = cursor.fetchone()
    sqllocation2 = row2[0]
    tmploc2 = sqllocation2.split(", ")
    strloc2 = tmploc2[1]
    print strloc2
    station = GasStation.objects.raw('SELECT * FROM gm_gasstation WHERE location LIKE %s or location LIKE %s', ("%" + strloc + "%","%" + strloc2 + "%",))
	#station = GasStation.objects.raw('SELECT * FROM gm_gasstation')

    cursor = connection.cursor()
    cursor.execute("SELECT address FROM tmpaddr")
    addre = cursor.fetchone()
    cursor.execute("SELECT address FROM tmpdest")
    deste = cursor.fetchone()
    return render(request, 'gm/trip.html', {'station_list': station, 'addr':addre[0], 'vmpg':locationzip, 'dest':deste[0]})

def predict(request, locationzip):
	cursor = connection.cursor()
	cursor.execute("SELECT address FROM tmpaddr")
	row = cursor.fetchone()
	sqllocation = row[0]
	tmploc = sqllocation.split(", ")
	strloc = tmploc[1]
	print strloc
	station = GasStation.objects.raw('SELECT * FROM gm_gasstation WHERE location LIKE %s', ("%" + strloc + "%",))
	#station = GasStation.objects.raw('SELECT * FROM gm_gasstation')

	cursor = connection.cursor()
	cursor.execute("SELECT address FROM tmpaddr")
	addre = cursor.fetchone()

	pre = []
	cursor = connection.cursor()
	cursor.execute('SELECT price FROM historydata ORDER BY month')
	weigh = [1,1,1,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
	cur = 0
	tot = 0.0
	hdata = cursor.fetchall()
	for ite in hdata:
		print float(ite[0])
		tot = tot + float(ite[0])*weigh[cur]
		cur += 1
	for st in station:
		cursor = connection.cursor()
		cursor.execute('SELECT price FROM priordata WHERE address = %s', (st.address,))
		par1 = cursor.fetchone()
		p2 = float(par1[0])
		if tot/9.0*0.8+p2*0.2 > float(st.price[1:]):
			pre.append("+")
		else:
			pre.append("-")
	return render(request, 'gm/predict.html', {'station_list': station, 'addr':addre[0], 'vmpg':locationzip, 'pre':pre})

@csrf_exempt
def getzipcode(request):
    if 'zipcode' in request.POST:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tmp")
        cursor.execute("""INSERT INTO tmp VALUES (%s)""",(request.POST['zipcode'],))
    return HttpResponse("Success")

@csrf_exempt
def getaddr(request):
    if 'address' in request.POST:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tmpaddr")
        cursor.execute("INSERT INTO tmpaddr(address) VALUES (%s)",(request.POST['address'],))
    return HttpResponse("Success")

@csrf_exempt
def getdest(request):
    if 'address' in request.POST:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tmpdest")
        cursor.execute("INSERT INTO tmpdest(address) VALUES (%s)",(request.POST['address'],))
    return HttpResponse("Success")

def recordmanager(request):
	#c = Car.objects.get(pk=request.POST['choice']).delete()
	#c.save()
	if 'add' in request.POST:
		return HttpResponseRedirect(reverse('gm:addcar'))

	if 'new' in request.POST:
		if request.POST['company'] == "" or request.POST['modeltype'] == "" or request.POST['madeyear'] == "" or request.POST['mpg'] == "" or request.POST['location'] == "":
			return HttpResponseRedirect(reverse('gm:index'))
		cursor = connection.cursor()
		cursor.execute("INSERT INTO gm_car(company, modeltype, madeyear, mpg, location) VALUES (%s,%s,%s,%s,%s)",(request.POST['company'],request.POST['modeltype'],request.POST['madeyear'],request.POST['mpg'],request.POST['location']))
		return HttpResponseRedirect(reverse('gm:index'))

	if 'edit' in request.POST:
		if 'choice' in request.POST:
			return HttpResponseRedirect(reverse('gm:editcar', args=(request.POST['choice'],)))

	if 'save' in request.POST:
		if request.POST['company'] == "" or request.POST['modeltype'] == "" or request.POST['madeyear'] == "" or request.POST['mpg'] == "" or request.POST['location'] == "":
			return HttpResponseRedirect(reverse('gm:index'))
		else:
			cursor = connection.cursor()
			cursor.execute ("""UPDATE gm_car SET company=%s, modeltype=%s, madeyear=%s, mpg=%s, location=%s WHERE id=%s""", (request.POST['company'], request.POST['modeltype'], request.POST['madeyear'], request.POST['mpg'], request.POST['location'], request.POST['id']))
			#c = Car(id = request.POST['id'],company = request.POST['company'], modeltype = request.POST['modeltype'], madeyear = request.POST['madeyear'], mpg = request.POST['mpg'], location = request.POST['location'])
			#c.save(force_update=True)
			return HttpResponseRedirect(reverse('gm:index'))

	if 'delete' in request.POST:
		if 'choice' in request.POST:
			#Car.objects.get(pk=request.POST['choice']).delete()
			cursor = connection.cursor()
			cursor.execute ("""DELETE FROM gm_car WHERE id=%s""", (request.POST['choice']))

	if 'search' in request.POST:
		if 'choice' in request.POST:
			#cursor = connection.cursor()
			#cursor.execute ("""DELETE FROM testdata""")
			str = Car.objects.get(pk=request.POST['choice']).mpg;
			print "haha"
			print str;
			#g = GasCrawler(str)
			#g.run()
			return HttpResponseRedirect(reverse('gm:result', args=(str,)))
	if 'trip' in request.POST:
		if 'choice' in request.POST:

			str = Car.objects.get(pk=request.POST['choice']).mpg;
			print "haha"
			print str;

			return HttpResponseRedirect(reverse('gm:trip', args=(str,)))

	if 'predict' in request.POST:
		if 'choice' in request.POST:
			#cursor = connection.cursor()
			#cursor.execute ("""DELETE FROM testdata""")
			str = Car.objects.get(pk=request.POST['choice']).mpg;
			print "haha"
			print str;
			#g = GasCrawler(str)
			#g.run()
			return HttpResponseRedirect(reverse('gm:predict', args=(str,)))


	return HttpResponseRedirect(reverse('gm:index'))


