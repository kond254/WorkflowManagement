import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})

// Klasse ermöglicht einen string Wert zwischen Componenten auszutauschen (Rolle)
export class RoleService {
    variable: string='';
  
    getRoleVariable(): string {
      return this.variable;
    }
  
    setRoleVariable(value: string): void {
      this.variable = value;
    }
  }