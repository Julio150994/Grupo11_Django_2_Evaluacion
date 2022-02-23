import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'api-django',
    loadChildren: () => import('./api-django/api-django.module').then( m => m.ApiDjangoPageModule)
  },
  {
    path: '',
    redirectTo: 'api-django',
    pathMatch: 'full'
  },
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
