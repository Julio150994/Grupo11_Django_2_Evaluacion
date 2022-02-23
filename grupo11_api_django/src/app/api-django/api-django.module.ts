import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { ApiDjangoPageRoutingModule } from './api-django-routing.module';

import { ApiDjangoPage } from './api-django.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ApiDjangoPageRoutingModule
  ],
  declarations: [ApiDjangoPage]
})
export class ApiDjangoPageModule {}
