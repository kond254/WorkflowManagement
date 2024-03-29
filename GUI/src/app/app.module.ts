import { NgModule} from '@angular/core';

import { AppRoutingModule } from './app-routing.module';

import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MatDialogModule } from '@angular/material/dialog';
import { DialogService } from './dialog.service';

import { FormsModule } from '@angular/forms';

import { FlexLayoutModule } from '@angular/flex-layout';

import { HttpClientModule } from '@angular/common/http';

import { MatAccordion } from '@angular/material/expansion';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatExpansionModule } from '@angular/material/expansion'; 
import { MatFormFieldModule } from '@angular/material/form-field'; 
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { MatSelectModule } from '@angular/material/select'; 
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatToolbarModule } from '@angular/material/toolbar'; 

import { NavbarComponent } from './navbar/navbar.component';

import { RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { AccountingComponent } from './accounting/accounting.component';
import { FooterComponent } from './footer/footer.component';
import { HomeComponent } from './home/home.component';
import { HrdepartmentComponent } from './hrdepartment/hrdepartment.component';
import { HrmanagerComponent } from './hrmanager/hrmanager.component';
import { LoginComponent } from './login/login.component';
import { DialogComponent } from './dialog/dialog.component';

import { SocketIoModule, SocketIoConfig } from 'ngx-socket-io';

const config: SocketIoConfig = { url: 'http://141.26.157.71:5000', options: {} };


@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    LoginComponent,
    HomeComponent,
    FooterComponent,
    AccountingComponent,
    HrdepartmentComponent,
    HrmanagerComponent,
    DialogComponent,
    
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    MatButtonModule,
    MatSidenavModule,
    MatIconModule,
    MatListModule,
    FormsModule,
    MatInputModule,
    FlexLayoutModule,
    MatFormFieldModule,
    MatCardModule,
    RouterModule,
    HttpClientModule,
    MatSelectModule,
    MatExpansionModule,
    MatDatepickerModule,
    MatDialogModule,
    SocketIoModule.forRoot(config)
   
  ],
  providers: [DialogService],
  bootstrap: [AppComponent]
  
})
export class AppModule { }