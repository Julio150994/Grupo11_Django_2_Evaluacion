import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AlertController } from '@ionic/angular';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiDjangoService {
  apiDjango = environment.api;// poner el enlace de la api en los entornos
  username: string;
  password: string;
  tok: any;
  token: any;
  cliente: any;
  id: number;

  constructor(private httpDjango: HttpClient, private alertCliente: AlertController) { }

  loginCliente(user, pwd) {
    return new Promise(res => {
      this.httpDjango.post<any>(this.apiDjango+'/token',{
        username: user,
        password: pwd
      }).subscribe(data => {
        console.log(data);
        this.cliente = data;
        this.cliente = this.cliente.data;
        localStorage.setItem('token',this.cliente);
        res(data);
      }, error => {
        this.clienteNoValido();// imprimimos un mensaje de alerta
        console.error('Error producido al iniciar sesión');
      });
    });
  }

  obtenerProyectosCliente() {
    // tok: any
    // .set('Authorization','Token '+tok)
    return new Promise(resolve => {
      this.httpDjango.get(this.apiDjango+'/proyectos_cli', {
        headers: new HttpHeaders().append('Content-Type','application/json')
      }).subscribe(res => {
        //console.log(res);
        resolve(res);
      }, (error) => {
        console.log(error);
      });
    });
  }

  async clienteNoValido() {
    const errorCliente = await this.alertCliente.create({
      header: 'ERROR',
      cssClass: 'loginCss',
      message: '<strong>Error producido al iniciar sesión</strong>',
      buttons: [
        {
          text: 'Aceptar',
          role: 'cancel',
          cssClass: 'secondary',
          handler: (valid) => {
          }
        }
      ]
    });
    await errorCliente.present();
  }
}
