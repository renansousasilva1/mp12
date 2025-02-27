from django.core.management.base import BaseCommand
from mapa.models import City

class Command(BaseCommand):
    help = "Adiciona todas as cidades ao banco de dados"

    def handle(self, *args, **kwargs):
        cities = [
            "Niterói", "Rio de Janeiro", "Itaguaí", "Mangaratiba", "Angra dos Reis",
            "Cabo Frio", "Arraial do Cabo", "Volta Redonda", "Paraty", "Nova Iguaçu",
            "Duque de Caxias", "São Gonçalo", "Campos dos Goytacazes", "São João de Meriti",
            "Macaé", "Petrópolis", "Teresópolis", "Magé", "Itaboraí", "Resende",
            "Queimados", "Maricá", "Barra Mansa", "Seropédica"
        ]

        for city_name in cities:
            city, created = City.objects.get_or_create(name=city_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Cidade adicionada: {city_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Cidade já existe: {city_name}'))

        self.stdout.write(self.style.SUCCESS("Todas as cidades foram processadas!"))
