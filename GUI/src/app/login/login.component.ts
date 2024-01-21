import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from '../dataAuth.service';
import { LoginService } from '../login.service';
import { RoleService } from '../role.service';
import { SnackbarService } from '../snackbar.service';
import { DataRoleService } from '../dataRole.service';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})

export class LoginComponent {

  username: string='';
  password: string='';
  errorType: string='';
  unvalidusername:boolean = false;
  unvalidpassword:boolean = false;
  loginUser: string='';
  role: string='';
  home: boolean = false;
  hrdepartment: boolean = false;
  hrmanagement: boolean = false;
  accounting: boolean = false;

  constructor(private router: Router, private dataService: DataService, private loginService: LoginService, private snackbarService: SnackbarService, private roleservice: RoleService,  private dataroleservice: DataRoleService) {}

  // Funktion überprüft, ob das Einloggen des Nutzer passt (nutzt den data.service.ts)
  login() {
    this.dataService.checkCredentials(this.username, this.password).subscribe((result) => {
      if (result == 'invalidPassword') {
        this.loginService.setloginValue(true);
        this.errorType = 'invalidPassword';
        this.unvalidusername = false;
        this.unvalidpassword = true;
        console.log('Login of username ' + this.username + ' not successful, because wrong password!');
      } else if (result == 'invalidUsername') {
        this.loginService.setloginValue(false);
        this.errorType = 'invalidUsername';
        this.unvalidusername = true;
        this.unvalidpassword = true;
        console.log('Login of username ' + this.username + ' not successful, because unauthorized user!');
      } else {
        this.loginService.setloginValue(true);
        this.role = result;
        console.log('Login of username ' + this.username + ' successful!');      
        this.handleSuccessfulLogin(result); 
        this.handle();
      }
    });
  }

  // Funktion wird in oberen If-Funktion aufgerufen
  private handleSuccessfulLogin(role: string) {
    this.unvalidusername = false;
    this.unvalidpassword = false;
    const routerLink = [''];
    this.router.navigate(routerLink);
    this.roleservice.setRoleVariable(this.role);
    console.log('Rights: ', role);
    this.snackbarService.showSuccess('Login successful!');
    }

    
  // Funktion ruft die Rechtes des eingeloggten Nutzer aus roleData.json ab und übergibt an dataRole.service.ts
  private handle(){
    const role: string = this.roleservice.getRoleVariable();
    this.dataroleservice.getRoleData(role).subscribe((data: any) => {
        this.home = data[role].home;
        this.hrdepartment = data[role].hrdepartment;
        this.hrmanagement = data[role].hrmanagement;
        this.accounting = data[role].accounting;
        this.dataroleservice.updateRechte(this.home , this.hrdepartment, this.hrmanagement, this.accounting);
      });
    }
  
}