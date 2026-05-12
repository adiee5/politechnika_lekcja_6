from src.manager import Manager
from src.models import Parameters, Tenant, Transfer

def test_totaldue():
    manager = Manager(Parameters())

    asettl=manager.get_settlement("apart-polanka", 2025, 1)

    tsettls=manager.create_tenants_settlements(asettl)

    s=0
    for tsett in tsettls:
        s += tsett.total_due_pln

    assert s == asettl.total_due_pln, f"Expected total due {asettl.total_due_pln}, got {s}"

def test_debtors():
    manager = Manager(Parameters())

    assert manager.get_debtors("apart-polanka", 2025, 1) == []

    manager.tenants["tenant-test"] = Tenant(name="Testownik", apartment="apart-polanka", rent_pln=10000.0, room= "room-bigger",
                                            deposit_pln= 3000.0, date_agreement_from= "2024-01-01", date_agreement_to= "2024-12-31")
    
    manager.transfers.append(Transfer(amount_pln=5000.0, date="2025-01-15", settlement_year=2025, settlement_month=1,
                                                     tenant="tenant-test"))
    
    assert manager.get_debtors("apart-polanka", 2025, 1) == ["tenant-test"]

def test_tax():
    manager = Manager(Parameters())

    assert manager.get_tax(2025, 1, 0.085) == 638
    assert manager.get_tax(2020, 1, 0.23) == 1725