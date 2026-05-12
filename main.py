from src.manager import Manager
from src.models import Parameters, ApartmentSettlement

import sys


def print_section_header(title: str):
    """Print a formatted section header"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def print_subsection_header(title: str):
    """Print a formatted subsection header"""
    print(f"\n  {title}")
    print(f"  {'-' * 40}")


def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"{amount:,.2f} PLN"


def display_apartments(manager):
    """Display all apartments with their rooms and bills"""
    print_section_header("APARTMENTS")
    
    for apartment in manager.apartments.values():
        print(f"\n📍 {apartment.name} ({apartment.key})")
        print(f"   Location: {apartment.location}")
        print(f"   Total Area: {apartment.area_m2} m²")
        
        print_subsection_header("Rooms")
        for room in apartment.rooms.values():
            print(f"      • {room.name:<25} {room.area_m2:>6} m²")
        
        # Find bills for this apartment
        apartment_bills = [bill for bill in manager.bills if bill.apartment == apartment.key]
        if apartment_bills:
            print_subsection_header("Bills")
            for bill in apartment_bills:
                month_year = f"{bill.settlement_month}/{bill.settlement_year}" if bill.settlement_month and bill.settlement_year else "N/A"
                print(f"      • {bill.type:<15} {format_currency(bill.amount_pln):>15}  Due: {bill.date_due}  Period: {month_year}")


def display_tenants(manager):
    """Display all tenants with their details and transfers"""
    print_section_header("TENANTS")
    
    for tenant in manager.tenants.values():
        print(f"\n👤 {tenant.name}")
        print(f"   Apartment: {tenant.apartment}")
        print(f"   Room: {tenant.room}")
        print(f"   Rent: {format_currency(tenant.rent_pln)}/month")
        print(f"   Deposit: {format_currency(tenant.deposit_pln)}")
        print(f"   Agreement: {tenant.date_agreement_from} to {tenant.date_agreement_to}")
        
        # Find transfers for this tenant
        tenant_transfers = [transfer for transfer in manager.transfers if transfer.tenant == tenant.name]
        if tenant_transfers:
            print_subsection_header("Transfers")
            for transfer in tenant_transfers:
                month_year = f"{transfer.settlement_month}/{transfer.settlement_year}" if transfer.settlement_month and transfer.settlement_year else "N/A"
                print(f"      • {format_currency(transfer.amount_pln):>15}  Date: {transfer.date}  Period: {month_year}")

def display_settlement(settlement: ApartmentSettlement|None):
    print_section_header("SETTLEMENT FROM COMMAND-LINE")
    if settlement==None:
        print("This settlement doesn't exist")

    print(f"\n🤝 {settlement.key}")

    total_due_pln: float
    total_transfers_pln: float = 0.0
    balance_pln: float = 0.0
    print(f"   Apartment: {settlement.apartment}")
    print(f"   Year: {settlement.year}")
    print(f"   Month: {settlement.month}")
    print(f"   Total Due: {format_currency(settlement.total_due_pln)}")
    print(f"   Total Transfers: {format_currency(settlement.total_transfers_pln)}")
    print(f"   Balance: {format_currency(settlement.balance_pln)}")

if __name__ == '__main__':
    parameters = Parameters()
    manager = Manager(parameters)

    display_apartments(manager)
    display_tenants(manager)

    if len(sys.argv)>=1+3:
        display_settlement(manager.get_settlement(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])))
    
    print(f"\n{'=' * 70}\n")