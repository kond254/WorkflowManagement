import { Injectable } from '@angular/core';
import { MatSnackBar, MatSnackBarConfig  } from '@angular/material/snack-bar';

@Injectable({
  providedIn: 'root'
})

export class SnackbarService {
  constructor(private snackBar: MatSnackBar) {}

  showSuccess(message: string): void {
    const snackBarConfig: MatSnackBarConfig = {  
      duration: 3000,
      horizontalPosition: 'end',
      verticalPosition: 'top',
      panelClass: ['snackbar'],
    };

    this.snackBar.open(message, 'Close', snackBarConfig);
  }
}
