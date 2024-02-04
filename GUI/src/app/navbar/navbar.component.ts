import { Component, OnInit, inject} from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { LoginService } from '../login.service';
import { RoleService } from '../role.service';
import { SnackbarService } from '../snackbar.service';
import { DataRoleService } from '../dataRole.service';
import { DataServiceInterface } from '../data.service';
import { SocketService } from '../socket.service';


@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})

export class NavbarComponent implements OnInit{

  home: boolean = false;
  showHome: boolean = false;
  hrdepartment: boolean = false;
  hrmanagement: boolean = false;
  accounting: boolean = false;
  role: string = '';

  constructor(public loginService: LoginService, private snackbarService: SnackbarService, private roleservice: RoleService, private dataroleservice: DataRoleService, private loginservice: LoginService,  private dataServiceInterface: DataServiceInterface, private socketService: SocketService) {
  }

  private breakpointObserver = inject(BreakpointObserver);

  ngOnInit(): void {
    this.dataServiceInterface.getLoginUsers().subscribe(
      loginUsers => {
        const isAnyUserLoggedIn = loginUsers.length;
        if(isAnyUserLoggedIn){
          console.log('Currently some users are logged in!');
          this.dataServiceInterface.getLoginUsers().subscribe(loginUsers => {
            const userIsLoggedIn = loginUsers.some(user => user.username == sessionStorage.getItem('currentLoggedUser') && user.isLoggedIn);
            if (userIsLoggedIn) {
              this.loginService.setloginValue(true);
              this.role = sessionStorage.getItem('currentRoleUser') as string || 'defaultRole';
              this.roleservice.setRoleVariable(this.role);
              this.updateRole();
            }
            else{
              this.loginService.setloginValue(false);
              this.role = '';
            }
          }); 

        }
        else{
          console.log('Currently no user is logged in!');
        }
      });
    this.socketService.onLoginUsersUpdated().subscribe(() => {
    this.updateLoginUsers();
  });
}

  updateLoginUsers(){
    this.dataServiceInterface.getLoginUsers().subscribe(
      loginUsers => {
        const isAnyUserLoggedIn = loginUsers.length;
        if(isAnyUserLoggedIn){
          console.log('Currently some users are logged in!');

        }
        else{
          console.log('Currently no user is logged in!');
        }
      });
  }


// Funktion ruft die Rechtes des eingeloggten Nutzer aus roleData.json ab und übergibt an dataRole.service.ts
private updateRole(){
  const role: string = this.roleservice.getRoleVariable();
  this.dataroleservice.getRoleData(role).subscribe((data: any) => {
      this.home = data[role].home;
      this.hrdepartment = data[role].hrdepartment;
      this.hrmanagement = data[role].hrmanagement;
      this.accounting = data[role].accounting;
      this.dataroleservice.updateRechte(this.home , this.hrdepartment, this.hrmanagement, this.accounting);
    });
  }


  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
    );
    

  // Funktion ruft die boolean Werte von dataRole.service auf
  get showRoleHome(): boolean {
    return this.dataroleservice.showRoleHome;
  }
  get showRoleHrdepartment(): boolean {
    return this.dataroleservice.showRoleHrdepartment;
  }
  get showRoleHrmanagement(): boolean {
    return this.dataroleservice.showRoleHrmanagement;
  }
  get showRoleAccouting(): boolean {
    return this.dataroleservice.showRoleAccouting;
  }


   // Funktion wird ausgeführt, wenn logout Button gedrückt wird und setzt dropdown Seiten auf standard false
   logout(){
    this.loginService.setloginValue(false);
    this.roleservice.setRoleVariable('');
    this.dataroleservice.updateRechte(this.showHome , this.hrdepartment, this.hrmanagement, this.accounting);

    const usernameDelete = sessionStorage.getItem('currentLoggedUser') as string || 'defaultUser';;
    this.dataServiceInterface.deleteLoginUser(usernameDelete).subscribe(response => {
      console.log(response);
    }, error => {
      console.error(error);
      });
      sessionStorage.removeItem('currentLoggedUser');
      sessionStorage.removeItem('currentRoleUser');
      console.log('Logout successful: ' + usernameDelete);
      this.snackbarService.showSuccess('Logout successful!');
    }  

}
