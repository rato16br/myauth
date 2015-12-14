#!/usr/local/bin/python3.4
__author__ = 'Fábio A. S. Sant Ana'

#import MySQLdib
import pymysql.cursors
import os

#Conectando o Banco Maluga
conexao = pymysql.connect(host="localhost", user="root", unix_socket='/var/run/mysql/mysql.sock', port='3306', passwd="tulipasql", db="admin")
cursor = conexao.cursor()

#Busca os clientes desativados com conexão Radius
sql1 = "select user from login where enable='0' and authradius='1'"
cursor.execute(sql1)

#Buscando o último login para ver se no mikrotik não esta logado com letras maiúsculas
for row in cursor.fetchall():
    cursor.execute("select username,nasipaddress from radius_acct where username='%s' order by radacctid desc limit 1"% (row[0]))
    for row2 in cursor.fetchall():
        if row2[0] is not None:
            #Dispara o comando para desconectar os clientes
            os.system("echo User-Name='%s' | radclient '%s':1700 disconnect raioceleste" % (row2[0], row2[1]))

cursor.close
