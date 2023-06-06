import {PlayerId, isPlayerId} from '../common/Types';
import {CardName} from '../common/cards/CardName';
import {ICorporationCard} from './cards/corporation/ICorporationCard';
import {Game} from './Game';
import {Payment} from '../common/inputs/Payment';
import {ICard, IActionCard, DynamicTRSource} from './cards/ICard';
import {TRSource} from '../common/cards/TRSource';
import {IProjectCard} from './cards/IProjectCard';
import {PlayerInput} from './PlayerInput';
import {Resource} from '../common/Resource';
import {CardResource} from '../common/CardResource';
import {SelectCard} from './inputs/SelectCard';
import {Priority} from './deferredActions/DeferredAction';
import {RobotCard} from './cards/promo/SelfReplicatingRobots';
import {SerializedPlayer} from './SerializedPlayer';
import {Timer} from '../common/Timer';
import {DrawCards} from './deferredActions/DrawCards';
import {Units} from '../common/Units';
import {IStandardProjectCard} from './cards/IStandardProjectCard';
import {GlobalParameter} from '../common/GlobalParameter';
import {GlobalEventName} from '../common/turmoil/globalEvents/GlobalEventName';
import {InputResponse} from '../common/inputs/InputResponse';
import {Tags} from './player/Tags';
import {Colonies} from './player/Colonies';
import {Production} from './player/Production';
import {ICeoCard} from './cards/ceos/ICeoCard';
import {IVictoryPointsBreakdown} from '..//common/game/IVictoryPointsBreakdown';
import {YesAnd} from './cards/requirements/CardRequirement';
import {PlayableCard} from './cards/IProjectCard';
import {Color} from '../common/Color';

export type ResourceSource = IPlayer | GlobalEventName | ICard;

export interface CanAffordOptions extends Partial<Payment.Options> {
  reserveUnits?: Units,
  tr?: TRSource | DynamicTRSource,
}

export interface IPlayer {
  readonly id: PlayerId;
  name: string;
  color: Color;
  beginner: boolean;
  handicap: number;

  game: Game;
  tags: Tags;
  colonies: Colonies;
  readonly production: Production;

  // Corporate identity
  corporations: Array<ICorporationCard>;

  // Used only during set-up
  pickedCorporationCard?: ICorporationCard;

  // Terraforming Rating
  hasIncreasedTerraformRatingThisGeneration: boolean;
  terraformRatingAtGenerationStart: number;

  // Resources
  megaCredits: number;
  steel: number;
  titanium: number;
  plants: number;
  energy: number;
  heat: number;

  // Helion
  canUseHeatAsMegaCredits: boolean;
  // Luna Trade Federation
  canUseTitaniumAsMegacredits: boolean;

  // This generation / this round
  actionsTakenThisRound: number;
  lastCardPlayed: CardName | undefined;
  pendingInitialActions: Array<ICorporationCard>;

  // Cards
  dealtCorporationCards: Array<ICorporationCard>;
  dealtPreludeCards: Array<IProjectCard>;
  dealtCeoCards: Array<ICeoCard>;
  dealtProjectCards: Array<IProjectCard>;
  cardsInHand: Array<IProjectCard>;
  preludeCardsInHand: Array<IProjectCard>;
  ceoCardsInHand: Array<IProjectCard>;
  playedCards: Array<IProjectCard>;
  draftedCards: Array<IProjectCard>;
  draftedCorporations: Array<ICorporationCard>;
  cardCost: number;
  needsToDraft?: boolean;

  timer: Timer;

  // Turmoil
  turmoilPolicyActionUsed: boolean;
  politicalAgendasActionUsedCount: number;

  oceanBonus: number;

  // Custom cards
  // Community Leavitt Station and Pathfinders Leavitt Station
  // TODO(kberg): move scienceTagCount to Tags?
  scienceTagCount: number;
  // PoliticalAgendas Scientists P41
  hasTurmoilScienceTagBonus: boolean;
  // Ecoline
  plantsNeededForGreenery: number;
  // Lawsuit
  removingPlayers: Array<PlayerId>;
  // For Playwrights corp.
  // removedFromPlayCards is a bit of a misname: it's a temporary storage for
  // cards that provide 'next card' discounts. This will clear between turns.
  removedFromPlayCards: Array<IProjectCard>;

  // The number of actions a player can take this round.
  // It's almost always 2, but certain cards can change this value.
  //
  // This value isn't serialized. Probably ought to.
  availableActionsThisRound: number;

  // Stats
  actionsTakenThisGame: number;
  victoryPointsByGeneration: Array<number>;
  totalDelegatesPlaced: number;

  tearDown(): void;
  tableau: Array<ICorporationCard | IProjectCard>;

  isCorporation(corporationName: CardName): boolean;
  getCorporation(corporationName: CardName): ICorporationCard | undefined;
  getCeo(ceoName: CardName): ICeoCard | undefined;
  getCorporationOrThrow(corporationName: CardName): ICorporationCard;
  getTitaniumValue(): number;
  increaseTitaniumValue(): void;
  decreaseTitaniumValue(): void;
  getSelfReplicatingRobotsTargetCards(): Array<RobotCard>;
  getSteelValue(): number;
  increaseSteelValue(): void;
  decreaseSteelValue(): void;
  getTerraformRating(): number;
  decreaseTerraformRating(opts?: {log?: boolean}): void;
  increaseTerraformRating(opts?: {log?: boolean}): void;
  increaseTerraformRatingSteps(steps: number, opts?: {log?: boolean}): void;
  decreaseTerraformRatingSteps(steps: number, opts: {log?: boolean}): void;
  setTerraformRating(value: number): void;
  getResource(resource: Resource): number;
  logUnitDelta(resource: Resource, amount: number, unitType: 'production' | 'amount', from: ResourceSource | undefined, stealing?: boolean): void;
  deductResource(
    resource: Resource,
    amount: number,
    options? :{
      log?: boolean,
      from? : ResourceSource,
      stealing?: boolean
    }): void;
  addResource(
    resource: Resource,
    amount: number,
    options? :{
      log?: boolean,
      from? : ResourceSource,
      stealing?: boolean
    }): void;
  /**
   * `from` steals up to `qty` units of `resource` from this player. Or, at least as
   * much as possible.
   */
  stealResource(resource: Resource, qty: number, thief: IPlayer): void;
  // Returns true when the player has the supplied units in its inventory.
  hasUnits(units: Units): boolean;
  addUnits(units: Partial<Units>, options? : {
    log?: boolean,
    from? : ResourceSource,
  }): void;
  deductUnits(units: Units): void;
  getActionsThisGeneration(): Set<CardName>;
  addActionThisGeneration(cardName: CardName): void;
  getVictoryPoints(): IVictoryPointsBreakdown;
  cardIsInEffect(cardName: CardName): boolean;
  hasProtectedHabitats(): boolean;
  plantsAreProtected(): boolean;
  alloysAreProtected(): boolean;
  canReduceAnyProduction(resource: Resource, minQuantity?: number): boolean;
  canHaveProductionReduced(resource: Resource, minQuantity: number, attacker: IPlayer): void;
  productionIsProtected(attacker: IPlayer): boolean;
  getNoTagsCount(): number;
  resolveInsurance(): void;
  resolveInsuranceInSoloGame(): void;
  getColoniesCount(): number;
  getPlayedEventsCount(): number;
  getRequirementsBonus(parameter: GlobalParameter): number;
  removeResourceFrom(card: ICard, count?: number, options?: {removingPlayer? : IPlayer, log?: boolean}): void;
  addResourceTo(card: ICard, options: number | {qty?: number, log: boolean, logZero?: boolean}): void;
  getCardsWithResources(resource?: CardResource): Array<ICard>;
  getResourceCards(resource?: CardResource): Array<ICard>;
  getResourceCount(resource: CardResource): number;
  deferInputCb(result: PlayerInput | undefined): void;
  runInput(input: InputResponse, pi: PlayerInput): void;
  getAvailableBlueActionCount(): number;
  getPlayableActionCards(): Array<ICard & IActionCard>;
  getUsableOPGCeoCards(): Array<ICeoCard>;
  runProductionPhase(): void;
  finishProductionPhase(): void;
  worldGovernmentTerraforming(): void;
  dealForDraft(quantity: number, cards: Array<IProjectCard>): void;
  askPlayerToDraft(initialDraft: boolean, playerName: string, passedCards?: Array<IProjectCard>): void;
  spendableMegacredits(): number;
  runResearchPhase(draftVariant: boolean): void;
  getCardCost(card: IProjectCard): number;
  getSpendableMicrobes(): number;
  getSpendableFloaters(): number;
  getSpendableScienceResources(): number;
  getSpendableSeedResources(): number;
  getSpendableData(): number;
  pay(payment: Payment): void;
  playCard(selectedCard: IProjectCard, payment?: Payment, cardAction?: 'add' | 'discard' | 'nothing' | 'action-only'): undefined;
  onCardPlayed(card: IProjectCard): void;
  playAdditionalCorporationCard(corporationCard: ICorporationCard): void;
  playCorporationCard(corporationCard: ICorporationCard): void;
  drawCard(count?: number, options?: DrawCards.DrawOptions): undefined;
  drawCardKeepSome(count: number, options: DrawCards.AllOptions): SelectCard<IProjectCard>;
  discardPlayedCard(card: IProjectCard): void;
  availableHeat(): number;
  spendHeat(amount: number, cb?: () => (undefined | PlayerInput)) : PlayerInput | undefined;
  pass(): void;
  takeActionForFinalGreenery(): void;
  getPlayableCards(): Array<PlayableCard>;
  // TODO(kberg): After migration, see if this can become private again.
  // Or perhaps moved into card?
  canAffordCard(card: IProjectCard): boolean;
  canPlay(card: IProjectCard): boolean | YesAnd;
  simpleCanPlay(card: IProjectCard): boolean | YesAnd;
  canSpend(payment: Payment, reserveUnits?: Units): boolean;
  payingAmount(payment: Payment, options?: Partial<Payment.Options>): number;
  canAfford(cost: number, options?: CanAffordOptions): boolean;
  getStandardProjectOption(): SelectCard<IStandardProjectCard>;
  takeAction(saveBeforeTakingAction?: boolean): void;
  runInitialAction(corp: ICorporationCard): void;
  getActions(): void;
  getWaitingFor(): PlayerInput | undefined;
  setWaitingFor(input: PlayerInput, cb?: () => void): void;
  setWaitingForSafely(input: PlayerInput, cb?: () => void): void;
  serialize(): SerializedPlayer;
  defer(input: PlayerInput | undefined, priority?: Priority): void;
}

export function isIPlayer(object: any): object is IPlayer {
  return object !== undefined && object.hasOwnProperty('id') && isPlayerId(object.id) && object.game instanceof Game;
}