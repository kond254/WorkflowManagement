import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from '../data.service';
import { LoginService } from '../login.service';
import { SnackbarService } from '../snackbar.service';
import { RoleService } from '../role.service';


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

  constructor(private router: Router, private dataService: DataService, private loginService: LoginService, private snackbarService: SnackbarService, private roleService: RoleService) {}

  // Funktion überprüft, ob das Einloggen des Nutzer passt (nutzt den data.service.ts)
  login() {
    this.dataService.checkCredentials(this.username, this.password).subscribe((result) => {
      if (result == 'valid') {
        this.loginService.setloginValue(true);
        this.unvalidusername = false;
        this.unvalidpassword = false;
        const routerLink = [''];
        this.router.navigate(routerLink);
        console.log('Login of username ' + this.username + ' successful!');
        this.snackbarService.showSuccess('Login erfolgreich!');
      } else {
        this.dataService.getUsers().subscribe((users) => {
          const userExists = users.some((u) => u.username === this.username);

          if (userExists) {
            this.loginService.setloginValue(false);
            this.errorType = 'invalidPassword';
            this.unvalidusername = false;
            this.unvalidpassword = true;
            console.log('Login of username ' + this.username + ' not successful, because wrong password!');
          } else {
            this.loginService.setloginValue(false);
            this.errorType = 'invalidUsername';
            this.unvalidusername = true;
            this.unvalidpassword = true;
            console.log('Login of username ' + this.username + ' not successful, because unauthorized user!');
          }
        });
      }
    });
  } 

  // Funktion liest die Rollenrechte der Nutzer (nutzt den data.service.ts)
  roleAccess(): void {
    this.dataService.getUsers().subscribe(users => {
      const isValidUser = users.find((u) => u.username == this.username && u.password == this.password);

      if (isValidUser) {
        console.log('User role is:', this.getUserRechte(this.username, users));
      } else {
        console.log('Login is failed. No rules!');
      }
    });
  }

  // Funktion gibt die Rollen rechte aus & legt boolean Werte fest & setzt die bool Werte für role.service.ts
  private getUserRechte(username: string, users: any[]): string | undefined {
    const user = users.find(u => u.username == username);
    this.role = user.role;

    if(this.role == 'admin'){
      this.home = true;
      this.hrdepartment = true;
      this.hrmanagement = true;
      this.accounting = true;
      console.log(this.home + ' ' +this.hrdepartment + ' ' + this.hrmanagement + ' ' + this.accounting);
      this.roleService.updateRechte(this.home , this.hrdepartment, this.hrmanagement, this.accounting);

    }else if(this.role =='normal'){
      this.home = true;
      this.hrdepartment = false;
      this.hrmanagement = false;
      this.accounting = false;
      console.log(this.home + ' ' +this.hrdepartment + ' ' + this.hrmanagement + ' ' + this.accounting);
      this.roleService.updateRechte(this.home , this.hrdepartment, this.hrmanagement, this.accounting);
  
    }else if(this.role =='accounting'){
      this.home = true;
      this.hrdepartment = false;
      this.hrmanagement = false;
      this.accounting = true;
      console.log(this.home + ' ' +this.hrdepartment + ' ' + this.hrmanagement + ' ' + this.accounting);
      this.roleService.updateRechte(this.home , this.hrdepartment, this.hrmanagement, this.accounting);
    
    }else{
      this.home = false;
      this.hrdepartment = false;
      this.hrmanagement = false;
      this.accounting = false;
      console.log(this.home + ' ' +this.hrdepartment + ' ' + this.hrmanagement + ' ' + this.accounting);
      this.roleService.updateRechte(this.home , this.hrdepartment, this.hrmanagement, this.accounting);
    }
    return user ? user.role : undefined;
  }
}