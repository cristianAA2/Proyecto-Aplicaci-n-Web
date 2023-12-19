from django.db import models
from datetime import datetime

class Atencion(models.Model):
    """
    @brief Modelo que representa una atención.

    Esta clase modela las atenciones realizadas en el sistema.

    Atributos:
        - id_atencion: Identificador único de la atención (AutoField).
        - estado: Estado de la atención (CharField, máximo 200 caracteres).
        - reserva: Indica si la atención es una reserva (BooleanField).
        - fecha: Fecha de la atención (DateField, por defecto la fecha actual).
        - hora: Hora de la atención (TimeField, por defecto la hora actual).
        - id_servicio: Relación con el modelo Servicio (ForeignKey).
        - rut_e: Relación con el modelo Empleado (ForeignKey).
        - id_cliente: Relación con el modelo Cliente (ForeignKey).
    """
    id_atencion = models.AutoField(db_column='id_atencion', primary_key=True)
    estado = models.CharField(max_length=200, blank=True, null=True)
    reserva = models.BooleanField(blank=False, null=False)
    fecha = models.DateField(default=datetime.now)
    hora = models.TimeField(default=datetime.now)
    id_servicio = models.ForeignKey('Servicio', models.DO_NOTHING, db_column='id_servicio')
    rut_e = models.ForeignKey('Empleado', models.DO_NOTHING, db_column='rut_e')
    id_cliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='id_cliente')

    class Meta:
        managed = True
        db_table = 'Atencion'


class Cliente(models.Model):
    """
    @brief Modelo que representa a un cliente.

    Esta clase modela la información de los clientes registrados en el sistema.

    Atributos:
        - id_cliente: Identificador único del cliente (CharField, máximo 50 caracteres).
        - nombre: Nombre del cliente (CharField, máximo 20 caracteres).
        - apellido: Apellido del cliente (CharField, máximo 20 caracteres).
        - fono: Número de teléfono del cliente (CharField, máximo 15 caracteres, opcional).
    """
    id_cliente = models.CharField(db_column='id_cliente', max_length=50, primary_key=True, unique=True)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    fono = models.CharField(max_length=15, blank=True)

    class Meta:
        managed = True
        db_table = 'Cliente'


class Empleado(models.Model):
    """
    @brief Modelo que representa a un empleado.

    Esta clase modela la información de los empleados registrados en el sistema.

    Atributos:
        - rut_e: Rut del empleado (CharField, máximo 10 caracteres, clave primaria).
        - nombre: Nombre del empleado (CharField, máximo 20 caracteres).
        - apellido: Apellido del empleado (CharField, máximo 20 caracteres).
    """
    rut_e = models.CharField(db_column='rut_e', primary_key=True, max_length=10)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'Empleado'


class Servicio(models.Model):
    """
    @brief Modelo que representa un servicio.

    Esta clase modela la información de los servicios ofrecidos en el sistema.

    Atributos:
        - id_servicio: Identificador único del servicio (AutoField).
        - nombre: Nombre del servicio (CharField, máximo 20 caracteres).
        - precio: Precio del servicio (IntegerField).
        - descripcion: Descripción del servicio (CharField, máximo 200 caracteres, opcional).
        - imagen: Imagen asociada al servicio (ImageField, se almacena en 'imagenes/').
    """
    id_servicio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    precio = models.IntegerField()
    descripcion = models.CharField(max_length=200, blank=True)
    imagen = models.ImageField(upload_to='imagenes/')

    class Meta:
        managed = True
        db_table = 'Servicio'