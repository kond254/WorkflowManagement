import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { DataAuthService } from '../dataAuth.service';
import { LoginService } from '../login.service';
import { RoleService } from '../role.service';
import { SnackbarService } from '../snackbar.service';
import { DataRoleService } from '../dataRole.service';
import { DataServiceInterface } from '../data.service';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})

//This class handles the login process and checks the access rights and sets roles rights and stores the logged in users
export class LoginComponent {

  hide = true;
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

  constructor(private router: Router, private dataAuthService: DataAuthService, private loginService: LoginService, private snackbarService: SnackbarService, private roleservice: RoleService,  private dataroleservice: DataRoleService, private dataServiceInterface: DataServiceInterface) {}

  //This method checks the results from dataAuth.service and decides whether the user has rights or not and displays the incorrect inputs as a hint message
  login() {
    console.log(this.username);
    console.log(this.password)
    this.dataAuthService.checkCredentials(this.username, this.password).subscribe((result) => {
      if (result == 'invalidPassword') {
          this.loginService.setloginValue(true);
          this.errorType = 'invalidPassword';
          this.unvalidusername = false;
          this.unvalidpassword = true;
          console.log('User loggin was not successful: ' + this.username);
          console.log('User has entered an incorrect password!');
      } else if (result == 'invalidUsername') {
          this.loginService.setloginValue(false);
          this.errorType = 'invalidUsername';
          this.unvalidusername = true;
          this.unvalidpassword = true;
          console.log('User loggin was not successful: ' + this.username);
          console.log('User has entered an unauthorized username!');
      } else {
          this.dataServiceInterface.setLoginUser(this.username, true).subscribe(response => {
          sessionStorage.setItem('currentLoggedUser',this.username);
          this.loginService.setloginUser(this.username);
          this.loginService.setloginValue(true);
          sessionStorage.setItem('currentRoleUser',result);
          this.role = result;   
          this.handleSuccessfulLogin(result); 
          this.updateRole();
          console.log('User loggin was successful: ' + this.username);
          console.log('User has the right: ' + this.role);
          console.log("User login has been recorded!");
          });   
        }
      });
  }

  //This method calls the home page with successful login and sets boolean values to false
  private handleSuccessfulLogin(role: string) {
    this.unvalidusername = false;
    this.unvalidpassword = false;
    const routerLink = [''];
    this.router.navigate(routerLink);
    this.roleservice.setRoleVariable(this.role);
    this.snackbarService.showSuccess('Login successful!');
    }

    
  //This method updates the current role rights of the logged-in user and saves them in dataRole.service.ts
  private updateRole(){
    const role: string = this.roleservice.getRoleVariable();
    this.dataroleservice.getRoleData(role).subscribe((data: any) => {
        this.home = data[role].home;
        this.hrdepartment = data[role].hrdepartment;
        this.hrmanagement = data[role].hrmanagement;
        this.accounting = data[role].accounting;
        this.dataroleservice.updateRoles(this.home , this.hrdepartment, this.hrmanagement, this.accounting);
      });
    }
  
}