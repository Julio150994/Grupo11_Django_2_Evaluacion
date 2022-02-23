import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ApiDjangoPage } from './api-django.page';

const routes: Routes = [
  {
    path: '',
    component: ApiDjangoPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class ApiDjangoPageRoutingModule {}
