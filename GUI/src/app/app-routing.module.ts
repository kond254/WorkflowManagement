import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { HrdepartmentComponent } from './hrdepartment/hrdepartment.component';
import { HrmanagerComponent } from './hrmanager/hrmanager.component';
import { AccountingComponent } from './accounting/accounting.component';

const routes: Routes = [
  { path: '', component: HomeComponent},
  { path: 'login', component: LoginComponent },
  { path: 'hrdepartment', component: HrdepartmentComponent },
  { path: 'hrmanager', component: HrmanagerComponent },
  { path: 'accounting', component: AccountingComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
