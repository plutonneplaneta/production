from config.database import SessionLocal
from models.transfer_loss import TransferLoss

def report_transfer_loss(
    order_id: int,
    route_id: int,
    material_id: int,
    expected_quantity: float,
    actual_quantity: float,
    loss_reason: str,
    recorded_date: str,
    recorded_by: int
):
    db = SessionLocal()
    try:
        loss = TransferLoss(
            order_id=order_id,
            route_id=route_id,
            material_id=material_id,
            expected_quantity=expected_quantity,
            actual_quantity=actual_quantity,
            loss_reason=loss_reason,
            recorded_date=recorded_date,
            recorded_by=recorded_by
        )
        db.add(loss)
        db.commit()
        db.refresh(loss)
        return loss
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_losses_by_order_id(db, order_id: int):
    return db.query(TransferLoss).filter(TransferLoss.order_id == order_id).all()