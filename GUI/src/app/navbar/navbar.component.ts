import { Component, inject} from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { LoginService } from '../login.service';
import { RoleService } from '../role.service';
import { SnackbarService } from '../snackbar.service';
import { DataRoleService } from '../dataRole.service';


@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})

export class NavbarComponent{

  showHome: boolean = false;
  hrdepartment: boolean = false;
  hrmanagement: boolean = false;
  accounting: boolean = false;

  constructor(public loginService: LoginService, private snackbarService: SnackbarService, private roleservice: RoleService, private dataroleservice: DataRoleService, private loginservice: LoginService) {
  }

  private breakpointObserver = inject(BreakpointObserver);

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
    this.snackbarService.showSuccess('Logout successful!');
    this.roleservice.setRoleVariable('');
    console.log('Logout successful!');
    this.dataroleservice.updateRechte(this.showHome , this.hrdepartment, this.hrmanagement, this.accounting);
  }  

}
