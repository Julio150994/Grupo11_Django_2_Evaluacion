import { Component, OnInit } from '@angular/core';
import { NavController } from '@ionic/angular';
import { ApiDjangoService } from '../services/api-django.service';

@Component({
  selector: 'app-api-django',
  templateUrl: './api-django.page.html',
  styleUrls: ['./api-django.page.scss'],
})
export class ApiDjangoPage implements OnInit {
  proyectos: any;
  proyectosCliente: any[] = [];
  tok: any;
  token: any;
  usuario: any;
  cliente: any;
  user: string;
  password: string;

  constructor(private apiService: ApiDjangoService, private navCtrl: NavController) { }

  ngOnInit() {
    console.log('Inicio');
  }

  async getProyectos() {
    const fechaActual = new Date();

    const formatoFecha = fechaActual.getFullYear()+'/'+fechaActual.getMonth()+1+'/'+fechaActual.getDate();

    console.log('Historial de proyectos en los que participa el cliente');
 
    // Iniciamos sesión con los datos de usuario (tipo cliente)
    /*await this.apiService.loginCliente(this.user, this.password)
    .then(async data => {
      this.tok = data;
      console.log(this.tok);
      this.cliente = this.tok.data;
      this.token = this.cliente.data;
      console.log(this.token);
      localStorage.setItem('token',this.token);

      if (this.token != null) {
        this.apiService.obtenerProyectosCliente(localStorage.getItem('token'))
        .then(proyectos => {
          this.proyectos = proyectos;
          if (this.proyectos != null) {
            for (let i = 0; i < this.proyectos?.length; i++) {
              this.proyectosCliente.push(this.proyectos[i]);
            }
          }
          else {
            console.error('No se han encontrado proyectos donde haya participado este cliente.');
          }
        });
      }
      else {
        console.error('Error al iniciar sesión.');
      }
    });*/

    // localStorage.getItem('token')
    this.apiService.obtenerProyectosCliente()
    .then(proyectos => {
      this.proyectos = proyectos;
      if (this.proyectos != null) {
        for (let i = 0; i < this.proyectos?.length; i++) {
          this.proyectosCliente.push(this.proyectos[i]);
        }
      }
      else {
        console.error('No se han encontrado proyectos donde haya participado este cliente.');
      }
    });
  }

}
